import os
from dotenv import load_dotenv
from smolagents import CodeAgent, LiteLLMModel
from tools import *

load_dotenv()

model = LiteLLMModel(
    model_id="groq/llama-3.1-8b-instant", 
    api_key=os.getenv("GROQ_API_KEY")
)

agent = CodeAgent(
    tools=[
        # —— Basic Controls ——————
        play_track, pause_playback, resume_playback,
        skip_next, skip_previous, set_shuffle,
        # —— Playlist Controls ———
        play_last_added_tracks, play_playlist,
        list_my_playlists,
        # —— Queue ———————————————
        add_to_queue,
        # —— Informations Tools ——
        get_current_track_info
    ],
    model=model,
    add_base_tools=False,
)
