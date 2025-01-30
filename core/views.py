import requests
import logging
import json

from .pages import *
from .search import *
from .extras import *
from slugify import slugify
from django.db.models import Q
from rest_framework import status
from requests import Request, post
from db.models import Artist, Album
from spotify.views import refresh_user
from rest_framework.views import APIView
from db.crud import get_token, create_collection, create_segment, get_spotify_song, create_song
from rest_framework.response import Response
from rest_framework.permissions import  AllowAny
from rest_framework.viewsets import GenericViewSet
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404

CLIENT_ID = os.environ.get('CLIENT_ID')
CLIENT_SECRET = os.environ.get('CLIENT_SECRET')
REDIRECT_URI = os.environ.get('REDIRECT_URI')

def home(request):
    return render(request, 'core/index.html')
    
def about(request):
    return render(request, 'core/about.html')

def login(request):
    return render(request, 'core/login.html')

def search(request):
    if request.method == "POST":
        query = request.POST['query']
        session_id = request.session.session_key
        print(f"Session ID: {session_id}")

        if session_id is None:
            return redirect('login')
        
        with get_db() as db:
            user = get_session_user(db, session_id)
            if user is None or not refresh_user(db, session_id):
                return redirect('login')
            authenticate_user(request.session, user.user_id)

            user_id = user.user_id
            token = get_token(db, user_id)
            if token is None:
                return redirect('login')
        
        sp = spotipy.Spotify(auth=token.access_token)
        response = sp.search(q=query, type='track,artist,album', limit=5)

        if "error" in response:
            return JsonResponse({}, status=204)
        
        t_data = response.get('tracks', {})
        tracks = t_data.get('items', [])
        lo_tracks = handle_tracks(tracks)

        a_data = response.get('albums', {})
        albums = a_data.get('items', [])
        lo_albums = handle_albums(albums)

        ar_data = response.get('artists', {})
        artists = ar_data.get('items', [])
        lo_artists = handle_artists(artists)

        return render(request, 'core/search.html', {
            'query': query,
            'tracks': lo_tracks,
            'albums': lo_albums,
            'artists': lo_artists
        })
    else:
        return render(request, 'core/search.html', {})
    
def artist_search(request):
    query = request.GET.get('q')
    print(f"Query: {query}")
    session_id = request.session.session_key
    print(f"Session ID: {session_id}")

    if session_id is None:
        return redirect('login')
    
    with get_db() as db:
        user = get_session_user(db, session_id)
        if user is None or not refresh_user(db, session_id):
            return redirect('login')
        authenticate_user(request.session, user.user_id)

        user_id = user.user_id
        token = get_token(db, user_id)
        if token is None:
            return redirect('login')
    
    sp = spotipy.Spotify(auth=token.access_token)
    response = sp.search(q=query, type='artist', limit=3)
    
    if "error" in response:
        return JsonResponse({}, status=204)

    ar_data = response.get('artists', {})
    artists = ar_data.get('items', [])
    lo_artists = handle_artists(artists)

    print("Artists: ", lo_artists)

    return render(request, 'partials/results.html', {'artists': lo_artists})

def save_artist_selection(request):
    if request.method == "POST":
        data = json.loads(request.body)
        segments = data.get("segments", [])
        session_id = request.session.session_key

        # Ensure user session exists
        if session_id is None:
            return JsonResponse({"error": "Not authenticated"}, status=401)

        with get_db() as db:
            user = get_session_user(db, session_id)
            if user is None or not refresh_user(db, session_id):
                return redirect('login')
            authenticate_user(request.session, user.user_id)

            user_id = user.user_id
            token = get_token(db, user_id)
            if token is None:
                return redirect('login')

            for segment in segments:
                artist_id = segment.get("artist_id")
                start_time = segment.get("start_time")
                end_time = segment.get("end_time")
                spotify_song_id = segment.get("spotify_song_id")

                song = get_spotify_song(spotify_song_id)
                collection = create_collection(db, song.song_id, None, None)
                    
                # Save to the database
                print(f"Saving: Artist {artist_id}, Start {start_time}, End {end_time}")
                create_segment(db, collection.collection_id, user.user_id, start_time, end_time, None, None)

        return JsonResponse({"success": True})

    return JsonResponse({"error": "Invalid request method"}, status=400)
    
def artist_page(request, artist_name, artist_id):
    artist = populate_artist(artist_id)
    artist_formatted = artist['name']
    
    html_content = render(request, 'core/artist_page.html', {'artist': artist, 'artist_name': artist_formatted}).content
    response = HttpResponse(html_content)
    response['Content-Type'] = 'text/html'
    return response

def album_page(request, artist_name, album_title, album_id):
    album = populate_album(album_id)
    album_formatted = album['title']
    
    html_content = render(request, 'core/album_page.html', {'album': album, 'album_title': album_formatted}).content
    response = HttpResponse(html_content)
    response['Content-Type'] = 'text/html'
    return response

def track_page(request, artist_name, track_title, track_id):
    track = populate_track(track_id)
    track_formatted = track['title']

    if get_spotify_song(track['spotify_song_id']) is None:
        with get_db() as db:
            create_song(db, track['spotify_song_id'], track['title'], track['artist'], track['artist_id'], track['album'], track['album_id'], track['cover'], track['release_year'], track['track_length'])

    html_content = render(request, 'core/edit_partition.html', {'track': track, 'track_title': track_formatted}).content
    response = HttpResponse(html_content)
    response['Content-Type'] = 'text/html'
    return response