import os

from datetime import timedelta
from db.models import User, Token
from rest_framework import status
from django.utils import timezone
from requests import Request, post
from django.shortcuts import redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from db.crud import create_token, get_token, get_spotify_user, update_user, create_user

CLIENT_ID = os.environ.get('CLIENT_ID')
CLIENT_SECRET = os.environ.get('CLIENT_SECRET')
REDIRECT_URI = os.environ.get('REDIRECT_URI')

AUTH_URL = 'https://accounts.spotify.com/authorize'
TOKEN_URL = 'https://accounts.spotify.com/api/token'
API_BASE_URL = 'https://api.spotify.com/v1/'

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

    if not request.session.exists(request.session.session_key):
        request.session.create()

    user = create_user(request.session.session_key, request.session.session_key)
    user_id = user.user_id
    print("user id: ")
    print(user_id)
    create_token(user_id,
                access_token, 
                refresh_token, 
                expires_in, 
                token_type)
    
    return redirect('core:index')

def is_authenticated(session_id):
    user = get_spotify_user(session_id)

    if user: 
        token = get_token(user.user_id)
        expiry_time = token.expires_in
        if expiry_time <= timezone.now():
            refresh = refresh_token(session_id)
            spotify_user_id = token.spotify_user_id
            user_with_id = get_spotify_user(spotify_user_id)
            update_user(user_with_id, is_authenticated=True, token=refresh)
        return True
    return False

def refresh_token(session_id):
    user = get_spotify_user(session_id)
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
        session_id = self.request.session.session_key
        is_auth = is_authenticated(session_id)
        return Response({'status': is_auth}, status=status.HTTP_200_OK)
