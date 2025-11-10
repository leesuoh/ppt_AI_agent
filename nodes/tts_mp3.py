import os
from openai import OpenAI
from utils import safe_run, save_state_log
from ffmpeg import probe

TTS_MODEL = os.getenv("TTS_MODEL", "gpt-4o-mini-tts")

def ffprobe_duration(path):
    try:
        info = probe(path)
        return float(info["format"]["duration"])
    except:
        return 0.0


@safe_run
def node_tts(state):
    client = OpenAI()
    script = state["script"]
    voice = state["prompt"].get("voice", "alloy")
    work_dir = state["work_dir"]

    audio_path = os.path.join(work_dir, "narration.mp3")
    with client.audio.speech.with_streaming_response.create(
        model=TTS_MODEL,
        voice=voice,
        input=script
    ) as response:
        response.stream_to_file(audio_path)

    duration = ffprobe_duration(audio_path)
    print(f"🎤 음성 파일 생성 완료 ({duration:.1f}초)")
    state["audio"] = audio_path
    save_state_log(state, "tts_mp3")
    return state
