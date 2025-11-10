import gradio as gr
from pipeline import lecture_graph
from utils import ensure_dir
import os, time

OUTPUT_DIR = ensure_dir("output")

def run_pipeline(ppt_file, tone, style, voice):
    if ppt_file is None:
        return "⚠️ PPT 파일을 업로드하세요.", None
    
    ppt_path = ppt_file.name
    work_dir = ensure_dir(os.path.join(OUTPUT_DIR, f"run_{int(time.time())}"))
    prompt = {"tone": tone, "style": style, "voice": voice}

    init_state = {
        "pptx_path": ppt_path,
        "slide_index": 0,
        "work_dir": work_dir,
        "prompt": prompt
    }

    yield "📄 PPT 분석 중...", None
    result = lecture_graph.invoke(init_state)

    if result.get("video_path"):
        yield "✅ 강의 영상 생성 완료!", result["video_path"]
    else:
        yield f"⚠️ 오류 발생: {result.get('error', '원인 미상')}", None


with gr.Blocks() as demo:
    gr.Markdown("## 🎓 AI 강의 영상 자동 제작기")
    ppt_file = gr.File(label="📁 PPT 업로드", file_types=[".pptx"])
    tone = gr.Radio(["부드럽게", "자신있게", "설명식"], label="톤 선택", value="부드럽게")
    style = gr.Radio(["친근하게", "전문적으로", "간결하게"], label="스타일", value="친근하게")
    voice = gr.Radio(["alloy", "verse", "aria"], label="TTS 음성", value="alloy")

    btn = gr.Button("🎬 강의 영상 생성")
    status = gr.Textbox(label="진행상황", interactive=False)
    video = gr.Video(label="🎞 결과 영상")

    btn.click(fn=run_pipeline, inputs=[ppt_file, tone, style, voice], outputs=[status, video])

demo.launch(share=True)
