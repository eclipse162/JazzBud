import re, os
import spotipy
from db.crud import create_song
from spotipy.oauth2 import SpotifyClientCredentials
from .search import handle_albums, handle_tracks, handle_artists
from django.shortcuts import render, redirect, get_object_or_404
from core.extras import authenticate_user, check_authentication, spotify_request_send

CLIENT_ID = os.environ.get('CLIENT_ID')
CLIENT_SECRET = os.environ.get('CLIENT_SECRET')

def populate_artist(artist_id):
    artist_data = retrieve_artist_data(artist_id)
    related_artists = handle_artists(artist_data['related']['artists'])

    top_tracks = handle_tracks(artist_data['top_tracks']['tracks'][0:4])
    popular_albums = sort_albums(top_tracks, artist_data['albums']['items'])

    artist = handle_artists([artist_data['artist']])[0]
    artist['related'] = related_artists
    artist['top_tracks'] = top_tracks
    artist['albums'] = handle_albums(popular_albums)

    return artist

def populate_album(album_id):
    album_data = retrieve_album_data(album_id)
    track_full = album_data['tracks']['items']
    album_info = album_data['album']

    tracklist = handle_album_tracks(track_full)
    album = handle_albums(album_info)[0]
    album['tracklist'] = tracklist

    return album

def handle_artists(artists):
    lo_artists = []
    for artist in artists:
        lo_artists.append({
            'artist_id': artist['id'],
            'cover': artist['images'][0]['url'],
            'name': artist['name']
        })
    return lo_artists

def retrieve_artist_data(artist_id):
    sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET))
    artist_data = {
        'artist': sp.artist(artist_id),
        'albums': sp.artist_albums(artist_id, album_type='album', limit=4),
        'related': sp.artist_related_artists(artist_id),
        'top_tracks': sp.artist_top_tracks(artist_id, country='US')
    }; return artist_data

def retrieve_album_data(album_id):
    sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET))
    album_data = {
        'album': sp.album(album_id),
        'tracks': sp.album_tracks(album_id)
    }; return album_data

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

    for track in tracks:
        album = track['album']
        if album['id'] not in album_ids:
            popular_albums.append(album)
            album_ids.add(album['id'])

    for album in albums:
        if len(popular_albums) >= 4:
            break
        if album['id'] not in album_ids:
            popular_albums.append(album)
            album_ids.add(album['id'])

    return popular_albums