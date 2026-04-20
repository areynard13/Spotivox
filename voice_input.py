import speech_recognition as sr

def listen_command():
    """
    Transcribe the user voice and stop automaticly when the user don't speak
    """
    recognizer = sr.Recognizer()
    
    recognizer.dynamic_energy_threshold = True
    recognizer.pause_threshold = 0.8

    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        
        try:
            audio = recognizer.listen(source, timeout=10, phrase_time_limit=15)
            print("Transcribing...")
            text = recognizer.recognize_whisper(audio, model="base", language="french")
            return text.strip()
            
        except sr.WaitTimeoutError:
            return "Timeout: No speech detected."
        except Exception as e:
            return f"Error: {e}"
