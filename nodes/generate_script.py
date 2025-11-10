import os
from openai import OpenAI
from utils import safe_run, save_state_log

LLM_MODEL = os.getenv("LLM_MODEL", "gpt-4.1-mini")

@safe_run
def node_generate_script(state):
    client = OpenAI()
    page_content = state["page_content"]
    prompt = state["prompt"]
    work_dir = state["work_dir"]

    sys_msg = "당신은 발표 스크립트 작성 전문가입니다. 60~90초 분량으로 작성해주세요."
    user_msg = f"""
    아래 내용을 기반으로 발표 스크립트를 작성해주세요.
    말투: {prompt.get('tone')}
    구조: 인트로 → 설명 → 마무리
    내용:\n{page_content}
    """

    resp = client.chat.completions.create(
        model=LLM_MODEL,
        messages=[
            {"role": "system", "content": sys_msg},
            {"role": "user", "content": user_msg}
        ],
        temperature=0.5,
        max_tokens=800
    )

    script_text = resp.choices[0].message.content.strip()
    state["script"] = script_text

    script_path = os.path.join(work_dir, "script.txt")
    with open(script_path, "w", encoding="utf-8") as f:
        f.write(script_text)

    save_state_log(state, "generate_script")
    return state
