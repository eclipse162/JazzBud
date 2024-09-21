import os
import requests
from db.models import Token
from db.database import get_db
from django.utils import timezone
from datetime import datetime, timedelta
from requests import post, get
from sqlalchemy.orm import session
from db.crud import create_token, get_token, get_session_user, get_user
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

CLIENT_ID = os.environ.get('CLIENT_ID')
CLIENT_SECRET = os.environ.get('CLIENT_SECRET')
REDIRECT_URI = os.environ.get('REDIRECT_URI')
BASE_URL = 'https://api.spotify.com/v1/me/'
TOKEN_URL = 'https://accounts.spotify.com/api/token'

def authenticate_user(session, user_id):
    session['user_id'] = user_id

def check_authentication(session_key, session):
    user_data = session.get(session_key)
    token = None

    if user_data:
        user_id = user_data.get('user_id')
        if user_id:
            with get_db() as db:
                token = get_token(db, user_id)
                expiry_time = token.expires_in

                if expiry_time.tzinfo is None:
                    expiry_time = timezone.make_aware(expiry_time, timezone.get_default_timezone())

                if expiry_time <= timezone.now():
                    token = refresh_token(user_data['session_id'])
                    with get_db() as db:
                        user = get_user(db, user_id)
                        user.token = token
                        db.commit()
        if token:
            return True, token.access_token
        
    return False, None

def spotify_request_send(session, session_key, endpoint, params={}):
    user_data = session.get(session_key)
    if not user_data:
        return {'Error': 'No user data found in session'}
    
    user_id = user_data.get('user_id')
    if not user_id:
        return {'Error': 'No user ID found in session data'}
    
    token = get_token(user_id)
    if not token:
        return {'Error': 'No tokens found for the session'}
    
    headers = {'Content-Type' : 'application/json', 
               'Authorization' : 'Bearer ' + token.access_token}
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
    
# def refresh_token(session_id):
#     user = get_session_user(session_id)
#     cur_token = get_token(user.user_id)

#     refresh_token = cur_token.refresh_token if cur_token else None
    
#     if not refresh_token:
#         print("Error: No refresh token found for the user")
#         return {'Error': 'No refresh token found for the user'}

#     request_data = {
#         'grant_type': 'refresh_token',
#         'refresh_token': refresh_token,
#         'client_id': CLIENT_ID,
#         'client_secret': CLIENT_SECRET}

#     response = requests.post(TOKEN_URL, data=request_data)

#     if response.status_code == 200:
#         data = response.json()
#         token_type = data.get('token_type')
#         expires_in = data.get('expires_in')
#         access_token = data.get('access_token')
#         new_refresh = data.get('refresh_token', refresh_token)
#     else:
#         print("Error: Failed to retrieve tokens from Spotify")
#         print("Spotify API response status code:", response.status_code)
#         print("Spotify API response content:", response.content)
#         return {'Error': 'Failed to retrieve tokens from Spotify'}

#     if not access_token or not expires_in or not token_type:
#         print("Error: Invalid response from Spotify API")
#         return {'Error': 'Invalid response from Spotify API'}

#     refresh = create_token(user.user_id, access_token, new_refresh, expires_in, token_type)
#     return refresh


def refresh_token(session_id):
    with get_db() as db:
        user = get_session_user(db, session_id)
        if user and user.token:
            refresh_token = user.token.refresh_token
            request_data = {
                'grant_type': 'refresh_token',
                'refresh_token': refresh_token,
                'client_id': CLIENT_ID,
                'client_secret': CLIENT_SECRET
            }

            response = post(TOKEN_URL, data=request_data)

            if response.status_code != 200:
                logging.error(f"Error from Spotify token endpoint: {response.text}")
                return None

            try:
                response_data = response.json()
            except ValueError as e:
                logging.error(f"JSON decode error: {str(e)}; Response text: {response.text}")
                return None

            access_token = response_data.get('access_token')
            expires_in = response_data.get('expires_in')
            token_type = response_data.get('token_type')

            new_token = create_token(db, user.user_id,
                        access_token, 
                        refresh_token, 
                        expires_in, 
                        token_type)
            return new_token
    return None