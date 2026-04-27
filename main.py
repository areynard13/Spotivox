import os
import numpy as np
import pyaudio
from dotenv import load_dotenv

from agent import agent
from voice_input import listen_command
from voice_output import speak
from utils import load_wake_word_model, open_audio_stream

load_dotenv()

WAKE_WORD_MODEL   = os.getenv("WAKE_WORD_MODEL_PATH", "hey_jarvis")  # .onnx or built-in name
DETECTION_THRESHOLD = 0.5
WAKE_WORD_LABEL   = "Hey Spotivox"



def handle_command(command: str) -> None:
    if not command or command.startswith(("Timeout", "Error")):
        speak("Je n'ai pas compris, réessaie.")
        return

    print(f"[Spotivox] Commande : {command}")
    try:
        response = agent.run(command)
        print(f"[Spotivox] Response : {response}")
        speak(str(response))
    except Exception as e:
        print(f"[Spotivox] Agent Error : {e}")
        speak("Une erreur s'est produite.")


def run() -> None:
    oww = load_wake_word_model()
    pa  = pyaudio.PyAudio()
    stream = open_audio_stream(pa)

    print(f"[Spotivox] Listening — say «{WAKE_WORD_LABEL}» …")
    speak(f"Bonjour ! Je suis prêt. Dis {WAKE_WORD_LABEL} pour me parler.")

    try:
        while True:
            raw = stream.read(CHUNK_SAMPLES, exception_on_overflow=False)
            audio = np.frombuffer(raw, dtype=np.int16)

            predictions = oww.predict(audio)

            if any(score >= DETECTION_THRESHOLD for score in predictions.values()):
                print(f"\n[Spotivox] Keyword detected !")
                oww.reset()
                speak("Oui ?")

                command = listen_command()
                handle_command(command)

    except KeyboardInterrupt:
        print("\n[Spotivox] Stop.")
        speak("Au revoir !")

    finally:
        stream.stop_stream()
        stream.close()
        pa.terminate()


if __name__ == "__main__":
    run()