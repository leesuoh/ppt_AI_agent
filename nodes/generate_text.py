import base64, io
from PIL import Image as PILImage
from openai import OpenAI
import os
from utils import safe_run, save_state_log

LLM_MODEL = os.getenv("LLM_MODEL", "gpt-4.1-mini")

def clean_text(txt): return txt.replace("\n", " ").strip()

def img_to_data_url_safe(path: str, max_size: int = 512, quality: int = 50) -> str:
    img = PILImage.open(path)
    if img.mode in ("RGBA", "LA"):
        background = PILImage.new("RGB", img.size, (255, 255, 255))
        background.paste(img, mask=img.split()[-1])
        img = background
    else:
        img = img.convert("RGB")
    img.thumbnail((max_size, max_size))
    buffered = io.BytesIO()
    img.save(buffered, format="JPEG", quality=quality)
    b64 = base64.b64encode(buffered.getvalue()).decode("utf-8")
    return f"data:image/jpeg;base64,{b64}"


@safe_run
def node_generate_text(state):
    client = OpenAI()
    texts = state["texts"]
    tables = state["tables"]
    images = state["images"][:3]
    prompt = state["prompt"]

    table_str = ""
    if tables:
        table_str = "\n".join([" | ".join(r) for r in tables[0][:6]])

    sys = "당신은 PPT 요약 전문가입니다."
    content = f"""
    텍스트, 표, 이미지를 기반으로 PPT 내용을 요약 설명해줘.
    1. 텍스트: {texts},
    2. 표: {table_str},
    3. 스타일: {prompt.get('style')}
    반드시 지킬 것: 과장 금지, 4~6문장, 불릿 금지, 스타일 적용.
    """

    resp = client.chat.completions.create(
        model=LLM_MODEL,
        messages=[
            {"role": "system", "content": sys},
            {"role": "user", "content": content}
        ],
        temperature=0.5,
        max_tokens=800
    )

    result = resp.choices[0].message.content.strip()
    state["page_content"] = result
    save_state_log(state, "generate_text")
    return state
