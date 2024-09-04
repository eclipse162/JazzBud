from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.views import APIView
from rest_framework.permissions import  AllowAny
from django.http import HttpResponseRedirect
from requests import Request, post
from .extras import *
from .search import *
from db.crud import get_song
import requests


CLIENT_ID = os.environ.get('CLIENT_ID')
CLIENT_SECRET = os.environ.get('CLIENT_SECRET')
REDIRECT_URI = os.environ.get('REDIRECT_URI')


def home(request):
    return render(request, 'core/index.html')
    
def about(request):
    return render(request, 'core/about.html')

def login(request):
    return render(request, 'core/login.html')

def search_results(request):
    if request.method == "POST":
        query = request.POST['query']

        song_id = extract_track_id(query)

        #song_results = get_song(query.split("=")[1])
        song_results = get_song(song_id)

        if song_results:
            #return render(request, 'core/search_results.html', {'query': query, 'song_results': song_results})
            # TO-DO: format song results from Song object to pass to search results page
            song_dict = {
            'spotify_song_id': song_results.id,
            'title': song_results.title,
            'artist': song_results.artist,
            'album': song_results.album,
            'genre': song_results.genre,  # Genre info is not always available
            'release_year': song_results.release_year,
            'track_length': song_results.track_length / 1000  # Convert milliseconds to seconds
        }

            return render(request, 'core/search_results.html', {'query': query, 'song_results': song_dict})
        else:
            # TO-DO: add song to database first, then show search results 
            try:
                song_dict = create_song_from_url(query)
                return render(request, 'core/search_results.html', {'query': query, 'song_results': song_dict})
            
            except ValueError:
                return render(request, 'core/search_results.html', {'query': None, 'song_results': None})
    
    else:
        return render(request, 'core/search_results.html', {})
    

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

    create_tokens(auth_key, access_token, refresh_token, expires_in, token_type)

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

        auth_status, access_token = check_authentication(key)
        print(f'Auth status: {auth_status}, Access token: {access_token}')

        if auth_status:
            user_info = self.get_user(access_token)
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
