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
from db.models import Artist, Album, Instrument
from spotify.views import refresh_user, confirm_authentication
from rest_framework.views import APIView
from db.crud import get_token, create_collection, create_segment, get_spotify_song, create_song
from rest_framework.response import Response
from rest_framework.permissions import  AllowAny
from rest_framework.viewsets import GenericViewSet
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

CLIENT_ID = os.environ.get('CLIENT_ID')
CLIENT_SECRET = os.environ.get('CLIENT_SECRET')
REDIRECT_URI = os.environ.get('REDIRECT_URI')

class home(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        return Response({"message": "Welcome to JazzBud!"})
    
class about(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        return Response({"message": "About JazzBud"})
    
class login(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        return Response({"message": "Login to JazzBud"})

class search(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        query = request.POST.get('query', '')
        session_id = request.session.session_key

        token = confirm_authentication(session_id, request)

        sp = spotipy.Spotify(auth=token.access_token)
        response = sp.search(q=query, type='track,artist,album', limit=10)

        if "error" in response:
            return JsonResponse({}, status=204)
        
        t_data = response.get('tracks', {})
        tracks = t_data.get('items', [])
        lo_tracks = handle_tracks(tracks[0:5])

        a_data = response.get('albums', {})
        albums = a_data.get('items', [])
        lo_albums = handle_albums(albums)

        ar_data = response.get('artists', {})
        artists = ar_data.get('items', [])
        lo_artists = handle_artists(artists)

        return JsonResponse({
            'query': query,
            'tracks': lo_tracks,
            'albums': lo_albums,
            'artists': lo_artists
        })
    
class artist_search(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        query = request.POST.get('query', '')

        session_id = request.session.session_key

        token = confirm_authentication(session_id, request)
        
        sp = spotipy.Spotify(auth=token.access_token)
        response = sp.search(q=query, type='artist', limit=3)
        
        if "error" in response:
            return JsonResponse({}, status=204)

        ar_data = response.get('artists', {})
        artists = ar_data.get('items', [])
        lo_artists = handle_artists(artists)

        return JsonResponse({
            'artists': lo_artists
        })

class instrument_search(APIView):

    def post(self, request):
        query = request.POST.get('query', '')
        
        session_id = request.session.session_key
        if session_id is None:
            return redirect('login')
        
        with get_db() as db:
            user = get_session_user(db, session_id)
            if user is None or not refresh_user(db, session_id):
                return redirect('login')
            authenticate_user(request.session, user.user_id)

            try:
                instruments = db.query(Instrument).filter(
                    Instrument.name.ilike(f"%{query}%")
                ).all()


                instrument_results = [ 
                    {
                        "id": instrument.instrument_id, 
                        "name": instrument.name, 
                        "colour": instrument.colour
                    } for instrument in instruments
                ]

                return JsonResponse({
                    'instrument_data': instrument_results
                }, status=200)
        
            except SQLAlchemyError as e:
                logging.error(f"Database error: {e}")
                return JsonResponse({"error": "Database error occurred"}, status=500)


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
    

class artist(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        artist_id = request.POST.get('artistId')
        session_id = request.session.session_key

        confirm_authentication(session_id, request)
        artist = populate_artist(artist_id)

        return JsonResponse({
            "artist": artist
        })

class album(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        album_id = request.POST.get('albumId')
        session_id = request.session.session_key

        token = confirm_authentication(session_id, request)
        album = populate_album(album_id)
        artist_id = album['artist_id']

        sp = spotipy.Spotify(auth=token.access_token)
        t_artist = sp.artist(artist_id)
        artist_image = t_artist['images'][0]['url'] if len(t_artist['images']) > 0 else None

        return JsonResponse({
            "album": album,
            "artistImage": artist_image,
            "token": token.access_token
        })

class track(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        track_id = request.POST.get('trackId')
        session_id = request.session.session_key

        token = confirm_authentication(session_id, request)
        track = populate_track(track_id)

        return JsonResponse({
            "track": track,
            "token": token.access_token
        })

def transfer_playback(request, device_id):
    session_id = request.session.session_key

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
    sp.transfer_playback(device_id=device_id, force_play=False)

    return JsonResponse({"success": True})

def playback(request, track_uri, action, position_ms=None):
    session_id = request.session.session_key

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
    devices = sp.devices()

    
    for device in devices['devices']:
        if device['name'] == 'JBud Player':
            device_id = device['id']

    if action == 'pause':
        sp.pause_playback(device_id=device_id)
    elif action == 'play':
        sp.start_playback(device_id=device_id, uris=[track_uri])
    elif action == 'next':
        sp.next_track(device_id=device_id)
    elif action == 'prev':
        sp.previous_track(device_id=device_id)
    elif action == 'position':
        sp.seek_track(position_ms, device_id=device_id)
            
    return JsonResponse({"success": True})