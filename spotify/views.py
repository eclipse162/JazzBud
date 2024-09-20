import os
import logging
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
        logging.error(f"Spotify authorization error: {error}")
        return JsonResponse({'error': error}, status=status.HTTP_400_BAD_REQUEST)

    if not code:
        logging.error("Authorization code not found in request")
        return JsonResponse({'error': 'Authorization code not found'}, status=status.HTTP_400_BAD_REQUEST)

    request_data = {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': REDIRECT_URI,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET
    }

    logging.info(f"Requesting token with data: {request_data}")

    response = post(TOKEN_URL, data=request_data)

    # Check for errors in the response
    if response.status_code != 200:
        logging.error(f"Error from Spotify token endpoint: {response.text}")
        return JsonResponse({'error': 'Failed to retrieve tokens from Spotify'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        response_data = response.json()
    except ValueError as e:
        logging.error(f"JSON decode error: {str(e)}; Response text: {response.text}")
        return JsonResponse({'error': 'Invalid response from Spotify token endpoint'}, status=status.HTTP_400_BAD_REQUEST)

    refresh_token = response_data.get('refresh_token')
    access_token = response_data.get('access_token')
    expires_in = response_data.get('expires_in')
    token_type = response_data.get('token_type')

    user_info_response = requests.get(SPOTIFY_ME_URL, headers={'Authorization': f'Bearer {access_token}'})

    if user_info_response.status_code != 200:
        logging.error(f"Error fetching Spotify user info: {user_info_response.text}")
        return JsonResponse({'error': 'Failed to retrieve user info from Spotify'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        user_info = user_info_response.json()
    except ValueError as e:
        logging.error(f"JSON decode error: {str(e)}; Response text: {user_info_response.text}")
        return JsonResponse({'error': 'Invalid user info response from Spotify'}, status=status.HTTP_400_BAD_REQUEST)

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
            if 'Error' in refresh:
                return False
            update_user(user.user_id, token=refresh)
        return True

def refresh_token(session_id):
    user = get_session_user(session_id)
    cur_token = get_token(user.user_id)

    refresh_token = cur_token.refresh_token if cur_token else None
    
    if not refresh_token:
        print("Error: No refresh token found for the user")
        return {'Error': 'No refresh token found for the user'}

    request_data = {
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET}

    response = requests.post(TOKEN_URL, data=request_data)

    if response.status_code == 200:
        data = response.json()
        token_type = data.get('token_type')
        expires_in = data.get('expires_in')
        access_token = data.get('access_token')
        new_refresh = data.get('refresh_token', refresh_token)
    else:
        print("Error: Failed to retrieve tokens from Spotify")
        print("Spotify API response status code:", response.status_code)
        print("Spotify API response content:", response.content)
        return {'Error': 'Failed to retrieve tokens from Spotify'}

    if not access_token or not expires_in or not token_type:
        print("Error: Invalid response from Spotify API")
        return {'Error': 'Invalid response from Spotify API'}

    refresh = create_token(user.user_id, access_token, new_refresh, expires_in, token_type)
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
        print(f"Session ID: {session_id}")
        user = get_session_user(session_id)
        print(f"User: {user}")
        if not user:
            return {'error': 'User not found'}
        token = get_token(user.user_id)
        if not token:
            return {'error': 'Token not found'}
        access_token = token.access_token
        spotify_info = requests.get(SPOTIFY_ME_URL, headers={'Authorization': f'Bearer {access_token}'}).json()
        print(f"Spotify info: {spotify_info}")

        user_info = {
            'user_id': spotify_info.get('id'),
            'display_name': spotify_info.get('display_name'),
            'profile_url': (spotify_info.get('images')[0].get('url') 
                    if spotify_info.get('images') else None)
        }
        
        return user_info
    
    def get(self, request):
        user_info = self.populate_user_info(request)
        return JsonResponse(user_info)
