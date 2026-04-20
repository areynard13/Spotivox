import os
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
from smolagents import tool
from dotenv import load_dotenv
from rapidfuzz import process, utils

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
def play_track(song_name: str) -> str:
    """
    Searches for a specific song and starts playback
    Args:
        song_name: The name of the song to play
    """
    results = sp.search(q=song_name, limit=1, type='track')
    if results['tracks']['items']:
        uri = results['tracks']['items'][0]['uri']
        name = results['tracks']['items'][0]['name']
        sp.start_playback(uris=[uri])
        return f"Successfully started playing '{name}'."
    return f"Track '{song_name}' not found."

@tool
def pause_playback() -> str:
    """
    Pauses the current music playback
    """
    sp.pause_playback()
    return "Playback paused."

@tool
def resume_playback() -> str:
    """
    Resumes the current music playback.
    """
    sp.start_playback()
    return "Playback resumed."

@tool
def skip_next() -> str:
    """
    Skips to the next track in the queue.
    """
    sp.next_track()
    return "Skipped to the next track."

@tool
def skip_previous() -> str:
    """
    Skips to the previous track.
    """
    sp.previous_track()
    return "Skipped back to the previous track."

@tool
def set_shuffle(state: bool) -> str:
    """
    Toggles the shuffle mode on or off for the current playback.
    Args:
        state: True to enable shuffle, False to disable it.
    """
    try:
        sp.shuffle(state)
        return f"Shuffle mode set to {state}."
    except Exception as e:
        return f"Failed to set shuffle: {e}"

# ————— Playlist Controls ———————————————————————
@tool
def play_last_added_tracks(playlist_name: str, count: int) -> str:
    """
    Finds a playlist by name and plays the 'count' most recently added tracks.
    Args:
        playlist_name: The name or partial name of the playlist.
        count: The number of tracks to play
    """
    playlists = sp.current_user_playlists()
    target = next(
        (p for p in playlists['items'] if playlist_name.lower() in p['name'].lower()),
        None
    )

    if not target:
        return f"Playlist '{playlist_name}' not found."

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

    return f"Added the last {len(uris)} tracks from playlist '{target['name']}' to the queue."

@tool
def play_playlist(playlist_name: str) -> str:
    """
    Finds the best matching playlist by name and starts playing it.
    Args:
        playlist_name: The name or partial name of the playlist.
    """
    try:
        results = sp.current_user_playlists()
        if not results['items']:
            return "You don't have any playlists in your library."

        playlists_map = {p['name']: p['uri'] for p in results['items']}
        playlist_names = list(playlists_map.keys())

        match = process.extractOne(
            playlist_name, 
            playlist_names, 
            processor=utils.default_process,
            score_cutoff=60
        )

        if match:
            best_name, score, _ = match
            uri = playlists_map[best_name]

            sp.start_playback(context_uri=uri)
            return f"Playing your '{best_name}' playlist (match score: {int(score)}%)."

        top_5 = ", ".join(playlist_names[:5])
        return f"Could not find a match for '{playlist_name}'. Your top playlists are: {top_5}."

    except Exception as e:
        if "device" in str(e).lower():
            return "Error: No active Spotify device found. Please open Spotify on your phone first."
        return f"An error occurred: {str(e)}"

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
def add_to_queue(song_name: str) -> str:
    """
    Adds a song to the end of the current playback queue without stopping current music.
    Args:
        song_name: The name of the song to add.
    """
    results = sp.search(q=song_name, limit=1, type="track")
    if results['tracks']['items']:
        uri = results['tracks']['items'][0]['uri']
        sp.add_to_queue(uri=uri)
        return f"Added '{song_name}' to the queue."
    return f"Could not find track '{song_name}' to add to queue."

# ————— Informations Tools ——————————————————————
@tool
def get_current_track_info() -> str:
    """
    Returns the name and artist of the song currently playing.
    """
    track = sp.current_playback()
    if track and track['is_playing']:
        name = track['item']['name']
        artist = track['item']['artists'][0]['name']
        return f"Currently playing '{name}' by {artist}."
    return "No track is currently playing."
