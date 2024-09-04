import re, os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

CLIENT_ID = os.environ.get('CLIENT_ID')
CLIENT_SECRET = os.environ.get('CLIENT_SECRET')

def extract_track_id(url):
    match = re.search(r'spotify\.com\/track\/([a-zA-Z0-9]+)', url)
    if match:
        return match.group(1)
    return None

def get_track_details(track_id):
    sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=CLIENT_ID,
                                                               client_secret=CLIENT_SECRET))
    track = sp.track(track_id)
    return {
        'spotify_song_id': track['id'],
        'title': track['name'],
        'artist': track['artists'][0]['name'],
        'album': track['album']['name'],
        'genre': 'N/A',  # Genre info is not always available
        'release_year': track['album']['release_date'][:4],
        'track_length': track['duration_ms'] / 1000  # Convert milliseconds to seconds
    }

def create_song_from_url(track_url):
    track_id = extract_track_id(track_url)
    if track_id:
        track_details = get_track_details(track_id)
        return track_details
    else:
        raise ValueError("Invalid Spotify track URL")