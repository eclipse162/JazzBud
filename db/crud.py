import os
from datetime import timedelta
from django.utils import timezone
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Base, User, Song, Segment, Token

# Create SQLAlchemy engine
DATABASE_URL = os.getenv('DATABASE_URL')
# DATABASE_URL = "postgres://jazzbuddy:FRpSvLa0sq0T4ifn6N3oC5ac1NPKt73V@dpg-cn5d2hv109ks739tk7h0-a.oregon-postgres.render.com/jazzbudb"
engine = create_engine(DATABASE_URL)
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

# Create operations
def create_user(spotify_user_id, username, display_name=None,session_id = None, is_authenticated=False, token=None):
    new_user = User(spotify_user_id=spotify_user_id, username=username, display_name=display_name, session_id=None, is_authenticated=is_authenticated, token=token)
    session.add(new_user)
    session.commit()
    return new_user

def create_song(spotify_song_id, title, artist, album, genre, release_year, track_length):
    new_song = Song(spotify_song_id=spotify_song_id, title=title, artist=artist, album=album, genre=genre, release_year=release_year, track_length=track_length)
    session.add(new_song)
    session.commit()
    return new_song

def create_collection(song_id, collection_name, collection_description):
    new_collection = Collection(song_id=song_id, collection_name=collection_name, collection_description=collection_description)
    session.add(new_collection)
    session.commit()
    return new_collection

def create_segment(collection_id, user_id, segment_name, start_time, end_time, segment_description):
    new_segment = Segment(collection_id=collection_id, user_id=user_id, segment_name=segment_name, start_time=start_time, end_time=end_time, segment_description=segment_description)
    session.add(new_segment)
    session.commit()
    return new_segment

def create_token(user_id, access_token, refresh_token, expires_in, token_type):
    token = get_token(user_id)
    if user_id == None:
        return None
    expires_in = timezone.now() + timedelta(seconds=expires_in)
    tkn = token

    if token:
        tkn = session.query(Token).filter(Token.user_id == user_id).one()
        tkn.access_token = access_token
        tkn.refresh_token = refresh_token
        tkn.expires_in = expires_in
        tkn.token_type = token_type
    else:
        tkn = Token(user_id=user_id, access_token=access_token, refresh_token=refresh_token, expires_in=expires_in, token_type=token_type)
        session.add(tkn)

    session.commit()
    return tkn

# Read operations
def get_user(user_id):
    return session.query(User).filter(User.user_id == user_id).first()

def get_session_user(session_id):
    return session.query(User).filter(User.session_id == session_id).first()

def get_spotify_user(spotify_user_id):
    return session.query(User).filter(User.spotify_user_id == spotify_user_id).first()

def get_song_by_song_id(song_id):
    return session.query(Song).filter(Song.song_id == song_id).first()

def get_spotify_song(spotify_song_id):
    return session.query(Song).filter(Song.spotify_song_id == spotify_song_id).first()

def get_collection(collection_id):
    return session.query(Collection).filter(Collection.collection_id == collection_id).first()

def get_song_collections(song_id):
    return session.query(Collection).filter(Collection.song_id == song_id).all()

def get_segment(segment_id):
    return session.query(Segment).filter(Segment.segment_id == segment_id).first()

def get_token(user_id):
    user = session.query(User).filter(User.user_id == user_id).first()

    if user and user.token:
        return user.token
    else:
        return None

# Update operations
def update_user(user_id, spotify_user_id=None, username=None, display_name=None, is_authenticated=None, token=None):
    user = get_user(user_id)
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
        session.commit()
    return user

def update_song(song_id, spotify_song_id=None, title=None, artist=None, album=None, genre=None, release_year=None):
    song = get_song_by_song_id(song_id)
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
        session.commit()
    return song

def update_collection(collection_id, song_id=None, collection_name=None, collection_description=None):
    collection = get_collection(collection_id)
    if collection:
        if song_id:
            collection.song_id = song_id
        if collection_name:
            collection.collection_name = collection_name
        if collection_description:
            collection.collection_description = collection_description
        session.commit()
    return collection

def update_segment(segment_id, collection_id=None, user_id=None, segment_name=None, start_time=None, end_time=None, segment_description=None):
    segment = get_segment(segment_id)
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
        session.commit()
    return segment

# Delete operations
def delete_user(user_id):
    user = get_user(user_id)
    if user:
        session.delete(user)
        session.commit()
    return user

def delete_song(song_id):
    song = get_song_by_song_id(song_id)
    if song:
        session.delete(song)
        session.commit()
    return song

def delete_segment(segment_id):
    segment = get_segment(segment_id)
    if segment:
        session.delete(segment)
        session.commit()
    return segment

def delete_collection(collection_id):
    collection = get_collection(collection_id)
    if collection:
        session.delete(collection)
        session.commit()
    return collection
