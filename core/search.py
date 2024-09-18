import re, os
import spotipy
from db.crud import create_song
from spotipy.oauth2 import SpotifyClientCredentials

CLIENT_ID = os.environ.get('CLIENT_ID')
CLIENT_SECRET = os.environ.get('CLIENT_SECRET')

def handle_tracks(tracks):
    lo_tracks = []
    for track in tracks:
        for artist in track['artists']:
            lo_tracks.append({
                'artist': ', '.join(artist['name']),
                'artist_id': ', '.join(artist['id'])
            })
        lo_tracks.append({
            'spotify_song_id': track['id'],
            'title': track['name'],
            'album': track['album']['name'],
            'album_id': track['album']['id'],
            'cover': track['album']['images'][1]['url'] if len(track['album']['images']) > 1 else track['album']['images'][0]['url'],
            'release_year': track['album']['release_date'][:4] if 'release_date' in track['album'] else 'Unknown',
            'track_length': track['duration_ms'] / 1000
        })
    return lo_tracks

def handle_albums(albums):
    lo_albums = []

    for album in albums:
        for artist in album['artists']:
            lo_albums.append({
                'artist': ', '.join(artist['name']),
                'artist_id': ', '.join(artist['id'])
            })
        lo_albums.append({
            'spotify_album_id': album['id'],
            'cover': album['images'][1]['url'],
            'title': album['name'],
            'release_year': album['release_date'][:4]
        })
    return lo_albums

def handle_artists(artists):
    return [{
        'spotify_artist_id': artist['id'],
        'cover': artist['images'][1]['url'] if len(artist['images']) > 1 else artist['images'][0]['url'],
        'name': artist['name']
    } for artist in artists]

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

        song = create_song(track_details['spotify_song_id'],
                         track_details['title'],
                         track_details['artist'],
                         track_details['album'],
                         track_details['genre'],
                         track_details['release_year'],
                         track_details['track_length'],)
        
        return song
    else:
        raise ValueError("Invalid Spotify track URL")