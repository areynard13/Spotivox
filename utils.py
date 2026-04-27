import os
import openwakeword
from openwakeword.model import Model
import pyaudio

SAMPLE_RATE   = 16000
CHUNK_SAMPLES = 1280
FORMAT        = pyaudio.paInt16
CHANNELS      = 1


def check_dotenv_vars():
    """Check if the required vars are stored in the dotenv file"""
    required_vars = ["SPOTIPY_CLIENT_ID", "SPOTIPY_CLIENT_SECRET", "SPOTIPY_REDIRECT_URI", "GROQ_API_KEY"]
    missing = [var for var in required_vars if not os.getenv(var)]

    if missing:
        raise EnvironmentError(f"The following variables are missing from your .env file: {', '.join(missing)}")

def open_audio_stream(pa: pyaudio.PyAudio) -> pyaudio.Stream:
    return pa.open(
        rate=SAMPLE_RATE,
        channels=CHANNELS,
        format=FORMAT,
        input=True,
        frames_per_buffer=CHUNK_SAMPLES,
    )


def load_wake_word_model() -> Model:
    model_path = os.getenv("WAKE_WORD_MODEL_PATH")
    
    if model_path and os.path.isfile(model_path):
        target_model_path = model_path
    else:
        pretrained_paths = openwakeword.get_pretrained_model_paths()
        target_model_path = next(
            (p for p in pretrained_paths if "hey_jarvis" in p), 
            None
        )
        
        if not target_model_path:
            raise FileNotFoundError("Could not find the built-in 'hey_jarvis' model.")

    return Model(wakeword_model_paths=[target_model_path])