from .models import Token
from django.utils import timezone
from datetime import datetime, timedelta
from requests import post
from .credentials import CLIENT_ID, CLIENT_SECRET

BASE_URL = 'https://api.spotify.com/v1/'

# 1. Check tokens
def check_tokens(session_id):
    tokens = Token.objects.filter(user=session_id).first()
    if tokens:
        return tokens[0]
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
        tokens.save(update_fields=['access_token', 
                                   'refresh_token', 
                                   'expires_in', 
                                   'token_type'])
    else:
        tokens = Token(user=session_id, 
                       access_token=access_token, 
                       refresh_token=refresh_token, 
                       expires_in=expires_in, 
                       token_type=token_type)
        tokens.save()

#3. Check Authetnication

def check_authentication(session_id):
    tokens = check_tokens(session_id)
    if tokens:
        if tokens.expires_in <= timezone.now():
            pass
        return True
    return False

#4. Refresh Token 
def refresh_token(session_id):
    refresh_token = check_tokens(session_id)
    response = post('https://accounts.spotify.com/api/token', data={
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET
    }).json()

    access_token = response.get('access_token')
    expires_in = response.get('expires_in')
    token_type = response.get('token_type')

    create_tokens(session_id, access_token, refresh_token, expires_in, token_type)