import os
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
from smolagents import tool
from dotenv import load_dotenv

load_dotenv()

sp = Spotify(auth_manager=SpotifyOAuth(
    client_id=os.getenv('SPOTIPY_CLIENT_ID'),
    client_secret=os.getenv('SPOTIPY_CLIENT_SECRET'),
    redirect_uri=os.getenv('SPOTIPY_REDIRECT_URI'),
    scope="user-modify-playback-state,user-read-playback-state,playlist-read-private"
))

try:
    user_info = sp.current_user()
    print(f"Connect as : {user_info['display_name']}")
except Exception as e:
    print(f"Configuration error: {e}")

# ————— Basic Controls ——————————————————————————
@tool
def  play_track(song_name: str) -> bool:
    """
    Searches for a specific song and starts playback
    Args:
        song_name: The name of the song to play
    Return: bool - the success of the action
    """
    results = sp.search(q=song_name, limit=1, type='track')
    if results['tracks']['items']:
        uri = results['tracks']['items'][0]['uri']
        name = results['tracks']['items'][0]['name']
        sp.start_playback(uris=[uri])
        return True
    return False

@tool
def pause_playback() -> bool:
    """
    Pauses the current music playback
    Return: bool - the success of the action
    """
    sp.pause_playback()
    return True

@tool
def resume_playback() -> bool:
    """
    Resumes the current music playback.
    Return: bool - the success of the action
    """
    sp.start_playback()
    return True

@tool
def skip_next() -> bool:
    """
    Skips to the next track in the queue.
    Return: bool - the success of the action
    """
    sp.next_track()
    return True

@tool
def skip_previous() -> bool:
    """
    Skips to the previous track.
    Return: bool - the success of the action
    """
    sp.previous_track()
    return True
