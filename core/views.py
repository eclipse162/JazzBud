from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.views import APIView
from rest_framework.permissions import  AllowAny
from django.http import HttpResponseRedirect
from requests import Request, post
from .credentials import CLIENT_ID, CLIENT_SECRET, REDIRECT_URI
from .extras import *

def index(request):
    return render(request, 'core/index.html')

def about(request):
    return render(request, 'core/about.html')

def store_code(code: str, user_id: str):
        # Write code here for database storage stuff
        raise NotImplementedError

# Prepare a URL for the user to authenticate with Spotify
class SpotifyRequestUserAuth(GenericViewSet):
    scopes = "streaming \
              user-top-read \
              user-read-private \
              user-read-recently-played \
              playlist-read-private \
              playlist-modify-private \
              playlist-modify-public \
              user-read-playback-position"
    permission_classes = (AllowAny,)

    def getAuth(self, request):
        scopes = 'user-read-private user-read-email'
        url = request('GET', 'https://accounts.spotify.com/authorize', params={
            'scope': scopes,
            'response_type': 'code',
            'redirect_uri': REDIRECT_URI,
            'client_id': CLIENT_ID
        }).prepare().url
        return HttpResponseRedirect(url)
        # Redirect the spotify login page to the user

def spotify_redirect(request):
    code = request.GET.get('code')
    error = request.GET.get('error')

    if error:
         return error 
    
    response = post('https://accounts.spotify.com/api/token', data={
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
    redirect_url = ""
    return HttpResponseRedirect(redirect_url)

# Checking whether the user has been authenticated by spotify
class ConfirmAuth(APIView):
    permission_classes = (AllowAny,)

    def getAuth(self, request):
        key = self.request.session.session_key
        if not self.request.session.exists(key):
            self.request.session.create()
            key = self.request.session.session_key
        auth_status = check_authentication(key)

        if auth_status:
            # Wil be redirected to the current song details
            redirect_url = ""
            return HttpResponseRedirect(redirect_url)
        else:
            # Will redirect to spotify login page
            redirect_url = ""
            return HttpResponseRedirect(redirect_url)