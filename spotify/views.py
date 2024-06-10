import os
import requests

from datetime import timedelta
from db.models import User, Token
from rest_framework import status
from django.utils import timezone
from requests import Request, post
from django.http import JsonResponse
from django.shortcuts import redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from db.crud import create_token, get_token, get_session_user, get_spotify_user, update_user, create_user

CLIENT_ID = os.environ.get('CLIENT_ID')
CLIENT_SECRET = os.environ.get('CLIENT_SECRET')
REDIRECT_URI = os.environ.get('REDIRECT_URI')

API_BASE_URL = 'https://api.spotify.com/v1/'
SPOTIFY_ME_URL = 'https://api.spotify.com/v1/me'
AUTH_URL = 'https://accounts.spotify.com/authorize'
TOKEN_URL = 'https://accounts.spotify.com/api/token'

class AuthURL(APIView):
    def get(self, request, format=None):
        scopes = "streaming \
                user-top-read \
                user-read-private \
                user-read-recently-played \
                playlist-read-private \
                playlist-modify-private \
                playlist-modify-public \
                user-read-playback-position"
        
        params = {
            'scope': scopes,
            'response_type': 'code',
            'redirect_uri': REDIRECT_URI,
            'client_id': CLIENT_ID} 
        
        url = Request('GET', AUTH_URL, params=params).prepare().url
        return Response({'url': url}, status=status.HTTP_200_OK)

def auth_callback(request, format=None):
    code = request.GET.get('code')
    error = request.GET.get('error')

    if error:
        return error
    
    request_data = {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': REDIRECT_URI,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET}
    
    response = post(TOKEN_URL, data=request_data).json()

    refresh_token = response.get('refresh_token')
    access_token = response.get('access_token')
    expires_in = response.get('expires_in')
    token_type = response.get('token_type')

    user_info = requests.get(SPOTIFY_ME_URL, headers={'Authorization': f'Bearer {access_token}'}).json()
    spotify_user_id = user_info.get('id')
    spotify_display = user_info.get('display_name')

    if not request.session.session_key:
        request.session.create()
    session_id = request.session.session_key

    user = get_spotify_user(spotify_user_id)

    if user:
        user.session_id = session_id
        user.is_authenticated = True
    else:
        user = create_user(spotify_user_id=spotify_user_id, 
                           username=spotify_user_id, 
                           display_name=spotify_display, 
                           session_id=session_id, 
                           is_authenticated=True)
    
    new_token = create_token(user.user_id,
                access_token, 
                refresh_token, 
                expires_in, 
                token_type)
    
    update_user(user.user_id, token=new_token)
    return redirect('core:home')

def refresh_user(session_id):
    user = get_session_user(session_id)

    if user: 
        token = get_token(user.user_id)
        expiry_time = token.expires_in

        if expiry_time.tzinfo is None:
            expiry_time = timezone.make_aware(expiry_time, timezone.get_default_timezone())

        if expiry_time <= timezone.now():
            refresh = refresh_token(session_id)
            update_user(user.user_id, token=refresh)
        return True

def refresh_token(session_id):
    user = get_session_user(session_id)
    refresh_token = get_token(user.user_id).refresh_token

    request_data = {
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET}
    response = post(TOKEN_URL, data=request_data).json()
    
    token_type = response.get('token_type')
    expires_in = response.get('expires_in')
    access_token = response.get('access_token')
    refresh_token = response.get('refresh_token')

    refresh = create_token(user.user_id, access_token, refresh_token, expires_in, token_type)
    return refresh

class IsAuthenticated(APIView):
    def get(self, request, format=None):
        # Check if the session exists
        if not request.session.session_key:
            request.session.create()
        
        session_id = request.session.session_key
        user = get_session_user(session_id)
        is_auth = False

        if user != None:
            is_auth = refresh_user(session_id)

        return Response({'status': is_auth}, status=status.HTTP_200_OK)

class SpotifyAPI(APIView):
    def populate_user_info(self, request):
        session_id = request.session.session_key
        user = get_session_user(session_id)
        token = get_token(user)
        access_token = token.access_token
        
        spotify_info = requests.get(SPOTIFY_ME_URL, headers={'Authorization': f'Bearer {access_token}'}).json()

        user_info = {
            'user_id': spotify_info.get('id'),
            'display name': spotify_info.get('display_name'),
            'profile_url': spotify_info.get('images')[0].get('url')
        }
        
        return user_info
    
    def get(self, request):
        user_info = SpotifyAPI.populate_user_info(request)
        return JsonResponse(user_info)