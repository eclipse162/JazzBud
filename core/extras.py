import os
import requests
from db.models import Token
from db.database import get_db
from django.utils import timezone
from datetime import datetime, timedelta
from requests import post, get
from sqlalchemy.orm import session
from db.crud import create_token, get_token, get_session_user
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

CLIENT_ID = os.environ.get('CLIENT_ID')
CLIENT_SECRET = os.environ.get('CLIENT_SECRET')
REDIRECT_URI = os.environ.get('REDIRECT_URI')
BASE_URL = 'https://api.spotify.com/v1/me/'

def authenticate_user(session, session_key, user_id):
    session[session_key] = {'user_id': user_id}

def check_authentication(session_key, session):
    user_data = session.get(session_key)
    token = None

    if user_data:
        user_id = user_data.get('user_id')
        if user_id:
            token = get_token(user_id)
        if token:
            return True, token.access_token
        
    return token is not None

def spotify_request_send(session_id, endpoint, params={}):
    user = get_session_user(session_id)
    token = get_token(user.user_id)
    if not token:
        return {'Error': 'No tokens found for the session'}
    headers = {'Content-Type' : 'application/json', 'Authorization' : 'Bearer ' + token.access_token}
    response = get(BASE_URL + endpoint, headers=headers, params=params)

    if response:
        print(response)
    else:
        print('No Response! Error with request.')
        
    try:
        return response.json()
    except Exception as e:
        print("Error parsing response: {e}")
        return {'Error': 'Issue with request'}
    
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
