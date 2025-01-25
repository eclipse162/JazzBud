import re, os
import traceback
import spotipy
from db.crud import create_song
from spotipy.exceptions import SpotifyException
from spotipy.oauth2 import SpotifyClientCredentials
from .search import handle_albums, handle_tracks, handle_artists
from django.shortcuts import render, redirect, get_object_or_404
from core.extras import authenticate_user, check_authentication, spotify_request_send

CLIENT_ID = os.environ.get('CLIENT_ID')
CLIENT_SECRET = os.environ.get('CLIENT_SECRET')

def populate_artist(artist_id):
    artist_data = retrieve_artist_data(artist_id)
    top_tracks = handle_tracks(artist_data['top_tracks']['tracks'][0:5])
    popular_albums = sort_albums(top_tracks, artist_data['albums']['items'])

    artist = handle_artists([artist_data['artist']])[0]
    artist['top_tracks'] = top_tracks
    artist['albums'] = handle_albums(popular_albums)

    return artist

def populate_album(album_id):
    print(f"populate_album called with album_id: {album_id}")
    traceback.print_stack(limit=35)
    album_data = retrieve_album_data(album_id)
    track_data = album_data['tracks']['items']

    tracklist = handle_album_tracks(track_data)
    album = handle_albums([album_data])[0]
    album['tracklist'] = tracklist

    return album

def populate_track(track_id):
    try:
        track_data = retrieve_track_data(track_id)
        track = handle_tracks([track_data])[0]
        return track
    except SpotifyException as e:
        if e.http_status == 404:
            # Print the error and handle the case where the track is not found
            print(f"Track not found: {track_id}")
            return None
        else:
            # Print the error and re-raise the exception for other errors
            print(f"Spotify API error: {e}")
            raise
    except Exception as e:
        # Print any other unexpected errors
        print(f"Unexpected error: {e}")
        raise

def handle_artists(artists):
    lo_artists = []
    for artist in artists:
        lo_artists.append({
            'artist_id': artist['id'],
            'cover': artist['images'][0]['url'],
            'name': artist['name']
        })
    return lo_artists

def retrieve_track_data(track_id):
    sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET))
    track_data = sp.track(track_id)
    return track_data

def retrieve_artist_data(artist_id):
    sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET))
    artist_data = {
        'artist': sp.artist(artist_id),
        'albums': sp.artist_albums(artist_id, album_type='album', limit=4),
        # 'related': sp.artist_related_artists(artist_id),
        'top_tracks': sp.artist_top_tracks(artist_id, country='US')
    }; return artist_data

def retrieve_album_data(album_id):
    sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET))
    album_data = sp.album(album_id)
    return album_data

def handle_album_tracks(tracks):
    lo_tracks = []
    for track in tracks:
        artist_names = [artist['name'] for artist in track['artists']]
        artist_ids = [artist['id'] for artist in track['artists']]
        lo_tracks.append({
            'artist': ', '.join(artist_names),
            'artist_id': ', '.join(artist_ids),
            'spotify_song_id': track['id'],
            'title': track['name'],
            'track_length': track['duration_ms'],
            'track_number': track['track_number']
        })
    return lo_tracks

def sort_albums(tracks, albums):
    popular_albums = []
    album_ids = set()

    # Add albums from tracks
    for track in tracks:
        album_id = track['album_id']
        album_name = track['album']
        if album_id not in album_ids:
            popular_albums.append({
                'id': album_id,
                'name': album_name,
                'cover': track['cover'],
                'release_year': track['release_year'],
                'artists': [{'name': track['artist'], 'id': track['artist_id']}]
            })
            album_ids.add(album_id)

    # Add remaining albums if less than 4
    for album in albums:
        if len(popular_albums) >= 5:
            break
        if album['id'] not in album_ids:
            popular_albums.append({
                'id': album['id'],
                'name': album['name'],
                'cover': album['images'][0]['url'],
                'release_year': album['release_date'][:4] if 'release_date' in album else 'Unknown',
                'artists': [{'name': artist['name'], 'id': artist['id']} for artist in album['artists']]
            })
            album_ids.add(album['id'])

    return popular_albums