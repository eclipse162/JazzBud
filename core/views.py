import requests
import logging

from .pages import *
from .search import *
from .extras import *
from slugify import slugify
from db.models import Artist, Album
from rest_framework import status
from requests import Request, post
from spotify.views import refresh_user
from rest_framework.views import APIView
from db.crud import get_token, create_token
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
    
    html_content = render(request, 'core/edit_partition.html', {'track': track, 'track_title': track_formatted}).content
    response = HttpResponse(html_content)
    response['Content-Type'] = 'text/html'
    return response