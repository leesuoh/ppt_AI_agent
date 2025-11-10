from langgraph.graph import StateGraph, START, END
from utils import State
from nodes import node_parse_ppt, node_generate_text, node_generate_script, node_tts, node_make_video

builder = StateGraph(State)

builder.add_node("parse_ppt", node_parse_ppt)
builder.add_node("generate_page", node_generate_text)
builder.add_node("generate_script", node_generate_script)
builder.add_node("tts_mp3", node_tts)
builder.add_node("make_video", node_make_video)

builder.add_edge(START, "parse_ppt")
builder.add_edge("parse_ppt", "generate_page")
builder.add_edge("generate_page", "generate_script")
builder.add_edge("generate_script", "tts_mp3")
builder.add_edge("tts_mp3", "make_video")
builder.add_edge("make_video", END)

lecture_graph = builder.compile()

