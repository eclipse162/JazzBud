import re, os
import json
import spotipy
import requests
from db.database import get_db
from db.crud import create_instrument
from requests import request, get
from spotify.views import refresh_user
from spotipy.oauth2 import SpotifyClientCredentials

# from django.shortcuts import render, redirect, get_object_or_404
# from db.crud import create_album, get_album, create_artist, get_artist
# from db.crud import create_artist, create_album, get_token, get_session_user
# from core.extras import authenticate_user, check_authentication, spotify_request_send


CLIENT_ID = os.environ.get('CLIENT_ID')
CLIENT_SECRET = os.environ.get('CLIENT_SECRET')

def add_instruments():
    with open('core/instruments.json', 'r') as f:
        instruments = json.load(f)

    with get_db() as db:
        for name, colour in instruments.items():
            create_instrument(db, name, colour)
            print(f"Added {name} to the database")

def handle_tracks(tracks):
    lo_tracks = []
    for track in tracks:
        artist_names = [artist['name'] for artist in track['artists']]
        artist_ids = [artist['id'] for artist in track['artists']]
        lo_tracks.append({
            'artist': ', '.join(artist_names),
            'artist_id': ', '.join(artist_ids),
            'spotify_song_id': track['id'],
            'title': track['name'],
            'album': track['album']['name'],
            'album_id': track['album']['id'],
            'cover': track['album']['images'][1]['url'] if len(track['album']['images']) > 1 else track['album']['images'][0]['url'],
            'release_year': track['album']['release_date'][:4] if 'release_date' in track['album'] else 'Unknown',
            'track_length': track['duration_ms']
        })
    return lo_tracks

def handle_albums(albums):
    lo_albums = []
    for album in albums:
        artist_names = [artist['name'] for artist in album['artists']]
        artist_ids = [artist['id'] for artist in album['artists']]
        if 'images' in album and album['images']:
            cover_url = album['images'][1]['url'] if len(album['images']) > 1 else album['images'][0]['url']
        else:
            cover_url = album['cover']

        if 'release_date' in album:
            release_year = album['release_date'][:4]
        else:
            release_year = album['release_year']
            
        lo_albums.append({
            'artist': ', '.join(artist_names),
            'artist_id': ', '.join(artist_ids),
            'album_id': album['id'],
            'cover': cover_url,
            'title': album['name'],
            'release_year': release_year
        })
    return lo_albums

def handle_artists(artists):
    lo_artists = []
    for artist in artists:
        if artist['images']: 
            cover = artist['images'][1]['url'] if len(artist['images']) > 1 else artist['images'][0]['url']
        else:
            cover = None 
        lo_artists.append({
            'artist_id': artist['id'],
            'cover': cover,
            'name': artist['name']
        })
    return lo_artists

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
        'track_length': track['duration_ms']
    }