import os
import requests
from db.models import Token
from db.database import get_db
from django.utils import timezone
from datetime import datetime, timedelta
from requests import post, get
from db.crud import create_token, get_token, get_session_user, get_user
from django.shortcuts import render, redirect, get_object_or_404

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

def spotify_request_send(session, endpoint, params={}):
    
    user_id = session.get('user_id')
    if not user_id:
        return {'Error': 'No user ID found in session data'}
    
    with get_db() as db:
        token = get_token(db, user_id)
        if not token:
            return {'Error': 'No tokens found for the session'}
        
    headers = {'Content-Type' : 'application/json', 
               'Authorization' : 'Bearer ' + token.access_token}
    response = get(endpoint, headers=headers, params=params)

    if response.status_code == 200:
        return response.json
    else:
        return {'Error': 'Issue with request'}
    

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
                print(f"Error from Spotify token endpoint: {response.text}")
                return None

            try:
                response_data = response.json()
            except ValueError as e:
                print(f"JSON decode error: {str(e)}; Response text: {response.text}")
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