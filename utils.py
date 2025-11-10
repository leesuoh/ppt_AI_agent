import os, json, datetime
from typing import TypedDict, List, Dict

# === State 정의 ===
class State(TypedDict, total=False):
    pptx_path: str
    work_dir: str
    prompt: Dict
    slide_index: int

    texts: List[str]
    tables: List[List[List[str]]]
    images: List[str]
    slide_image: List[str]

    page_content: str
    script: str

    audio: str
    video_path: str


# === 공통 유틸 ===
def ensure_dir(path):
    os.makedirs(path, exist_ok=True)
    return path


def save_state_log(state, step):
    """각 노드 단계별 상태 저장"""
    os.makedirs("logs", exist_ok=True)
    filename = f"{datetime.datetime.now().strftime('%H%M%S')}_{step}.json"
    with open(os.path.join("logs", filename), "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)


def safe_run(func):
    """노드 예외 처리용 데코레이터"""
    def wrapper(state):
        try:
            result = func(state)
            result["ok"] = True
        except Exception as e:
            state["ok"] = False
            state["error"] = str(e)
            save_state_log(state, f"error_{func.__name__}")
            print(f"❌ Error in {func.__name__}: {e}")
            return state
        return result
    return wrapper
