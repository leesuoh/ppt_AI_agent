import os
from moviepy.editor import ImageClip, AudioFileClip
from utils import safe_run, save_state_log

MEDIA_DIR = "output"

def render_mp4(image_path, audio_path, output_path):
    img_clip = ImageClip(image_path).set_duration(AudioFileClip(audio_path).duration)
    audio_clip = AudioFileClip(audio_path)
    video = img_clip.set_audio(audio_clip)
    video.write_videofile(output_path, fps=24, codec="libx264", audio_codec="aac")


@safe_run
def node_make_video(state):
    slide_image = state["slide_image"][0]
    audio = state["audio"]
    slide_index = state["slide_index"]
    video_path = os.path.join(MEDIA_DIR, f"slide{slide_index}_lecture.mp4")

    render_mp4(slide_image, audio, video_path)
    state["video_path"] = video_path
    save_state_log(state, "make_video")
    return state
