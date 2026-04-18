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

@tool
def set_shuffle(state: bool) -> bool:
    """
    Toggles the shuffle mode on or off for the current playback.
    Args:
        state: True to enable shuffle, False to disable it.
    Return: bool - the success of the action
    """
    try:
        sp.shuffle(state)
        status = "enabled" if state else "disabled"
        return True
    except Exception as e:
        return False

# ————— Playlist Controls ———————————————————————
@tool
def play_last_added_tracks(playlist_name: str, count: int) -> dict:
    """
    Finds a playlist by name and plays the 'count' most recently added tracks.
    Args:
        playlist_name: The name or partial name of the playlist.
        count: The number of tracks to play
    Return: dict - the success of the action (success) with explanation if false (message)
    """
    playlists = sp.current_user_playlists()
    target = next(
        (p for p in playlists['items'] if playlist_name.lower() in p['name'].lower()),
        None
    )

    if not target:
        return {"success": False, "message": f"Playlist {playlist_name} not found"}

    total_tracks = target['items']['total']
    start_index = max(0, total_tracks - count)

    results = sp.playlist_items(
        target['id'], 
        limit=count, 
        offset=start_index
    )
    items = results['items'][::-1]
    uris = [item['item']['uri'] for item in items if item.get('item')]

    for uri in uris:
        sp.add_to_queue(uri)

    return {
        "success": True,
        "message": ""
    }

@tool
def play_playlist(playlist_name: str) -> bool:
    """
    Finds a playlist by name and starts playing it.
    Args:
        playlist_name: The name or part of the name of the playlist to start.
    Return: bool - the success of the action
    """
    results = sp.current_user_playlists()
    
    target_playlist = next(
        (p for p in results['items'] if playlist_name.lower() in p['name'].lower()), 
        None
    )
    
    if target_playlist:
        playlist_uri = target_playlist['uri']
        try:
            sp.start_playback(context_uri=playlist_uri)
            return True
        except Exception as e:
            return False
            
    return False

@tool
def list_my_playlists() -> str:
    """
    Retrieves the names of all your playlists. 
    Use this to verify if a playlist exists before trying to play it.
    Return: str - All playlists name separate by ','
    """
    playlists = sp.current_user_playlists()
    names = [p['name'] for p in playlists['items']]
    return ", ".join(names)

# ————— Queue ———————————————————————————————————
@tool
def add_to_queue(song_name: str) -> bool:
    """
    Adds a song to the end of the current playback queue without stopping current music.
    Args:
        song_name: The name of the song to add.
    Return: bool - the success of the action
    """
    results = sp.search(q=song_name, limit=1, type="track")
    if results['tracks']['items']:
        uri = results['tracks']['items'][0]['uri']
        sp.add_to_queue(uri=uri)
        return True
    return False

# ————— Informations Tools ——————————————————————
@tool
def get_current_track_info() -> dict:
    """
    Returns the name and artist of the song currently playing.
    """
    track = sp.current_playback()
    if track and track['is_playing']:
        name = track['item']['name']
        artist = track['item']['artists'][0]['name']
        return {'artist': artist, 'name': name}
    return {'artist': '', 'name': ''}
