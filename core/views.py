import requests
import logging

from .search import *
from .extras import *
from rest_framework import status
from requests import Request, post
from spotify.views import refresh_user
from rest_framework.views import APIView
from db.crud import get_token, create_token
from django.http import HttpResponseRedirect
from rest_framework.response import Response
from django.shortcuts import render, redirect
from rest_framework.permissions import  AllowAny
from rest_framework.viewsets import GenericViewSet

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

        if session_id is None:
            return redirect('core:login')
        
        with get_db() as db:
            user = get_session_user(db, session_id)
            if user is None or not refresh_user(db, session_id):
                return redirect('core:login')
            
        endpoint = "https://api.spotify.com/v1/search"
        params = {
            'q': query,
            'type': 'track, artist, album',
            'limit': 5
        }

        response = spotify_request_send(request.session, session_id, endpoint, params=params)

        if "error" in response:
            return Response({}, status=status.HTTP_204_NO_CONTENT)
        
        t_data = response.get('tracks', {})
        tracks = t_data.get('items', [])
        lo_tracks = handle_tracks(tracks)

        a_data = response.get('albums', {})
        albums = a_data.get('items', [])
        lo_albums = handle_albums(albums)

        ar_data = response.get('artists', {})
        artists = ar_data.get('items', [])
        lo_artists = handle_artists(artists)

        logging.info(f"Query: {query}")
        logging.info(f"Tracks: {lo_tracks}")
        logging.info(f"Albums: {lo_albums}")
        logging.info(f"Artists: {lo_artists}")

        return render(request, 'core/search.html', {
            'query': query,
            'tracks': lo_tracks,
            'albums': lo_albums,
            'artists': lo_artists
        })
    else:
        return render(request, 'core/search.html', {})
    

# Prepare a URL for the user to authenticate with Spotify
class SpotifyRequestUserAuth(APIView):
    scopes = "streaming \
              user-top-read \
              user-read-private \
              user-read-recently-played \
              playlist-read-private \
              playlist-modify-private \
              playlist-modify-public \
              user-read-playback-position"
    permission_classes = (AllowAny,)

    def get(self, request):
        scopes = 'user-read-private user-read-email'
        params = {
            'scope': scopes,
            'response_type': 'code',
            'redirect_uri': REDIRECT_URI,
            'client_id': CLIENT_ID
        }
        response = requests.get('https://accounts.spotify.com/authorize', params=params)
        url = response.url
        print("HELLO WORLD", flush=True)
        return HttpResponseRedirect(url)
        # Redirect the spotify login page to the user

def spotify_redirect(request):
    code = request.GET.get('code')
    error = request.GET.get('error')

    if error:
         return error 
    
    response = requests.post('https://accounts.spotify.com/api/token', data={
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': REDIRECT_URI,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET
    }).json()

    access_token = response.get('access_token')
    refresh_token = response.get('refresh_token')
    expires_in = response.get('expires_in')
    token_type = response.get('token_type')

    auth_key = request.session.session_key
    if not request.session.exists(auth_key):
        request.session.create()
        auth_key = request.session.session_key

    with get_db() as db:
        create_token(db, access_token, refresh_token, expires_in, token_type)
        db.commit()

    # Create a redirect url to the current song details
    redirect_url = f"http://127.0.0.1:8000/jazzbud/check-auth?key={auth_key}"
    return HttpResponseRedirect(redirect_url)

# Checking whether the user has been authenticated by spotify
class ConfirmAuth(APIView):
    permission_classes = (AllowAny,)

    def get_user(self, access_token):
        headers = {
            'Authorization': f'Bearer {access_token}',
        }
        response = requests.get('https://api.spotify.com/v1/me', headers=headers)
        print(f'Spotify API response status: {response.status_code}, body: {response.json()}', flush=True)
        if response.status_code == 200:
            return response.json()
        else:
            return None

    def get(self, request):
        key = self.request.session.session_key
        if not self.request.session.exists(key):
            self.request.session.create()
            key = self.request.session.session_key
        print(f'Session key: {key}', flush=True)

        with get_db() as db:
            auth_status, access_token = check_authentication(key, session)
            print(f'Auth status: {auth_status}, Access token: {access_token}')
            if auth_status:
                user_info = get_user(db, access_token)
                if user_info and user_info["type"] == "user":
                    user_id = user_info['id']
                    user_name = user_info['display_name']
                    user_pfp = user_info['images'][0]['url']
                    print(f'User ID: {user_id}, User Name: {user_name}', flush=True)
                else:
                    print('User info retrieval failed or incorrect user type.', flush=True)
                redirect_url = f"http://127.0.0.1:8000/jazzbud/check-auth?key={key}"
                return HttpResponseRedirect(redirect_url)
            else:
                redirect_url = f"http://127.0.0.1:8000/jazzbud/auth_url"
                return HttpResponseRedirect(redirect_url)
        
class CurrentSong(APIView):
    kwarg = "key"

    def get(self, request):
        key = request.GET.get(self.kwarg)
        token = Token.objects.filter(user=key)
        endpoint = "https://api.spotify.com/v1/me/player/currently-playing"
        response = spotify_request_send(key, endpoint)

        if "error" in response:
            return Response({}, status=status.HTTP_204_NO_CONTENT)
        
        item = response.get('item')
        duration = response.get('progress_ms')
        is_playing = response.get('is_playing')
        progress = response.get('progress_ms')
        timestamp = response.get('timestamp')
        song_id = item.get('id')
        title = item.get('name')
        album_cover = item.get('album').get('images')[0].get('url')
        artists = ""
        for i, artist in enumerate(item.get("artists")):
            if i > 0:
                artists += ", "
            name = artist.get('name')
            artists += name
        song = {
            "id": song_id,
            "title": title,
            "artists": artists,
            "album_cover": album_cover,
            "is_playing": is_playing,
            "progress": progress,
            "duration": duration,
            "timestamp": timestamp
        }

        print(song, flush=True)
        return Response(song, status = status.HTTP_200_OK)
