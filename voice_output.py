import os
import edge_tts
import asyncio
import pygame

VOICE = "fr-FR-DeniseNeural"

async def _generate_speech(text: str, output_file: str):
    communicate = edge_tts.Communicate(text, VOICE)
    await communicate.save(output_file)

def speak(text: str):
    """
    Transform a text in voice and play it
    """
    output_file = "response.mp3"
    asyncio.run(_generate_speech(text, output_file))

    pygame.mixer.init()
    pygame.mixer.music.load(output_file)
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
    
    pygame.mixer.quit()
    os.remove(output_file)
