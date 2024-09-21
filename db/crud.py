import os
from datetime import timedelta
from django.utils import timezone
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Base, User, Song, Segment, Token, Collection
from .database import get_db

# Create operations
def create_user(db, spotify_user_id, username, display_name=None,session_id = None, is_authenticated=False, token=None):
        new_user = User(spotify_user_id=spotify_user_id, username=username, display_name=display_name, session_id=session_id, is_authenticated=is_authenticated, token=token)
        db.add(new_user)
        return new_user

def create_song(db, spotify_song_id, title, artist, artist_id, album, album_id, cover, release_year, track_length):
    new_song = Song(spotify_song_id=spotify_song_id, title=title, artist=artist, artist_id=artist_id, album=album, album_id=album_id, cover=cover, release_year=release_year, track_length=track_length)
    db.add(new_song)
    return new_song

def create_collection(db, song_id, collection_name, collection_description):
    new_collection = Collection(song_id=song_id, collection_name=collection_name, collection_description=collection_description)
    db.add(new_collection)
    return new_collection

def create_segment(db, collection_id, user_id, segment_name, start_time, end_time, segment_description):
    new_segment = Segment(collection_id=collection_id, user_id=user_id, segment_name=segment_name, start_time=start_time, end_time=end_time, segment_description=segment_description)
    db.add(new_segment)
    return new_segment

def create_token(db, user_id, access_token, refresh_token, expires_in, token_type):
    if user_id == None:
        print('User ID is None', flush=True)
        return None
    
    expires_in = timezone.now() + timedelta(seconds=expires_in)
    token = db.query(Token).filter(Token.user_id == user_id).first()

    if token:
        token.access_token = access_token
        token.refresh_token = refresh_token
        token.expires_in = expires_in
        token.token_type = token_type
    else:
        token = Token(
            user_id=user_id, 
            access_token=access_token,
            refresh_token=refresh_token, 
            expires_in=expires_in, 
            token_type=token_type)
        db.add(token)
    return token

# Read operations
def get_user(db, user_id):
    return db.query(User).filter(User.user_id == user_id).first()

def get_spotify_user(db, spotify_user_id):
    return db.query(User).filter(User.spotify_user_id == spotify_user_id).first()

def get_session_user(db, session_id):
    return db.query(User).filter(User.session_id == session_id).first()

def get_song_by_song_id(db, song_id):
    return db.query(Song).filter(Song.song_id == song_id).first()

def get_spotify_song(db, spotify_song_id):
    return db.query(Song).filter(Song.spotify_song_id == spotify_song_id).first()

def get_collection(db, collection_id):
    return db.query(Collection).filter(Collection.collection_id == collection_id).first()

def get_song_collections(db, song_id):
    return db.query(Collection).filter(Collection.song_id == song_id).all()

def get_segment(db, segment_id):
    return db.query(Segment).filter(Segment.segment_id == segment_id).first()

def get_token(db, user_id):
    user = db.query(User).filter(User.user_id == user_id).first()

    if user and user.token:
        return user.token
        
    else:
        print('No token found for the user', flush=True)
        return None

# Update operations
def update_user(db, user_id, spotify_user_id=None, username=None, display_name=None, is_authenticated=None, token=None):
    user = get_user(db, user_id)
    if user:
        if spotify_user_id:
            user.spotify_user_id = spotify_user_id
        if username:
            user.username = username
        if is_authenticated:
            user.is_authenticated = is_authenticated
        if display_name:
            user.display_name = display_name
        if token:
            user.token = token
    return user

def update_song(db, song_id, spotify_song_id=None, title=None, artist=None, album=None, genre=None, release_year=None, track_length=None):
    song = get_song_by_song_id(db, song_id)
    if song:
        if spotify_song_id:
            song.spotify_song_id = spotify_song_id
        if title:
            song.title = title
        if artist:
            song.artist = artist
        if album:
            song.album = album
        if genre:
            song.genre = genre
        if release_year:
            song.release_year = release_year
        if track_length:
            song.track_length = track_length
    return song

def update_collection(db, collection_id, song_id=None, collection_name=None, collection_description=None):
    collection = get_collection(db, collection_id)
    if collection:
        if song_id:
            collection.song_id = song_id
        if collection_name:
            collection.collection_name = collection_name
        if collection_description:
            collection.collection_description = collection_description
    return collection

def update_segment(segment_id, collection_id=None, user_id=None, segment_name=None, start_time=None, end_time=None, segment_description=None):
    segment = get_segment(db, segment_id)
    if segment:
        if collection_id:
            segment.collection_id = collection_id
        if user_id:
            segment.user_id = user_id
        if segment_name:
            segment.segment_name = segment_name
        if start_time:
            segment.start_time = start_time
        if end_time:
            segment.end_time = end_time
        if segment_description:
            segment.segment_description = segment_description
    return segment

# Delete operations
def delete_user(db, user_id):
    user = get_user(db, user_id)
    if user:
        db.delete(user)
    return user

def delete_song(db, song_id):
    song = get_song_by_song_id(db, song_id)
    if song:
        db.delete(song)
    return song

def delete_segment(db, segment_id):
    segment = get_segment(db, segment_id)
    if segment:
        db.delete(segment)
    return segment

def delete_collection(db, collection_id):
    collection = get_collection(db, collection_id)
    if collection:
        db.delete(collection)
    return collection
