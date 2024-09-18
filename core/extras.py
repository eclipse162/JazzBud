import os
import requests
from db.models import Token
from django.utils import timezone
from datetime import datetime, timedelta
from requests import post, get
from sqlalchemy.orm import session

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

CLIENT_ID = os.environ.get('CLIENT_ID')
CLIENT_SECRET = os.environ.get('CLIENT_SECRET')
REDIRECT_URI = os.environ.get('REDIRECT_URI')
DATABASE_URL = os.environ.get('DATABASE_URL')
BASE_URL = 'https://api.spotify.com/v1/me/'

engine = create_engine(os.environ.get('DATABASE_URL'))
Session = sessionmaker(bind=engine)
session = Session()

# 1. Check tokens
def check_tokens(session_id):
    token = session.query(Token).filter_by(user_id=session_id).first()
    if token:
        return token
    else:
        return None

# 2. Create and update tokens
def create_tokens(session_id, access_token, refresh_token, expires_in, token_type):
    tokens = check_tokens(session_id)
    expires_in = timezone.now() + timedelta(seconds=expires_in)

    if tokens:
        tokens.access_token = access_token
        tokens.refresh_token = refresh_token
        tokens.expires_in = expires_in
        tokens.token_type = token_type
        session.commit()
        # tokens.save(update_fields=['access_token', 
        #                            'refresh_token', 
        #                            'expires_in', 
        #                            'token_type'])
    else:
        # tokens = Token(user=session_id, 
        #                access_token=access_token, 
        #                refresh_token=refresh_token, 
        #                expires_in=expires_in, 
        #                token_type=token_type)
        # tokens.save()
        session.add(tokens)
        session.commit()

#3. Check Authetnication

def check_authentication(session_id):
    tokens = check_tokens(session_id)
    if tokens:
        if tokens.expires_in <= timezone.now():
            refresh_token(session_id)
        return True
    return False

#4. Refresh Token 
def refresh_token(session_id):
    tokens = check_tokens(session_id)
    if not tokens:
        return {'Error': 'No tokens found for the session'}
    
    refresh_token = tokens.refresh_token
    response = requests.post('https://accounts.spotify.com/api/token', data={
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET
    }).json()

    print("SPOTIFY API RESPONSE", response)

    access_token = response.get('access_token')
    expires_in = response.get('expires_in')
    token_type = response.get('token_type')
    
    if not access_token or not expires_in or not token_type:
        return {'Error': 'Invalid response from Spotify'}
    
    # create_tokens(session_id=session_id, 
    #               access_token=access_token,
    #               refresh_token=refresh_token, 
    #               expires_in=expires_in, 
    #               token_type=token_type)

def spotify_request_send(session_id, endpoint, params={}):
    tokens = check_tokens(session_id)
    if not tokens:
        return {'Error': 'No tokens found for the session'}
    headers = {'Content-Type' : 'application/json', 'Authorization' : 'Bearer ' + tokens.access_token}
    response = get(BASE_URL + endpoint, headers=headers, params=params)

    if response:
        print(response)
    else:
        print('No Response! Error with request.')
        
    try:
        return response.json()
    except:
        return {'Error': 'Issue with request'}
