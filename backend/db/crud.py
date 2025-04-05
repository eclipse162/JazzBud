import os
import logging
from datetime import timedelta
from django.utils import timezone
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Base, User, Song, Segment, Token, Collection, Artist, Album, Instrument, SegmentArtist, Section
from .database import get_db

# User operations

def create_user(db, username: str, spotify_user_id: str, display_name: str):
    user = User(username=username, spotify_user_id=spotify_user_id, display_name=display_name)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def get_user(db, user_id: int):
    return db.query(User).filter(User.user_id == user_id).first()

def update_user(db, user_id: int, new_data: dict):
    user = db.query(User).filter(User.user_id == user_id).first()
    if user:
        for key, value in new_data.items():
            setattr(user, key, value)
        db.commit()
        db.refresh(user)
    return user

def delete_user(db, user_id: int):
    user = db.query(User).filter(User.user_id == user_id).first()
    if user:
        db.delete(user)
        db.commit()
    return user

# Proposed token operations

'''
def create_token(db, user_id: int, access_token: str, refresh_token: str, expires_in, token_type: str):
    token = Token(user_id=user_id, access_token=access_token, refresh_token=refresh_token, expires_in=expires_in, token_type=token_type)
    db.add(token)
    db.commit()
    db.refresh(token)
    return token

def get_token(db, token_id: int):
    return db.query(Token).filter(Token.token_id == token_id).first()

def delete_token(db, token_id: int):
    token = db.query(Token).filter(Token.token_id == token_id).first()
    if token:
        db.delete(token)
        db.commit()
    return token'
'''

# Artist operations

def create_artist(db, sp_artist_id: str, name: str, cover: str):
    artist = Artist(sp_artist_id=sp_artist_id, name=name, cover=cover)
    db.add(artist)
    db.commit()
    db.refresh(artist)
    return artist

def create_instrument(db, name, colour):
    new_instrument = Instrument(name=name, colour=colour)
    db.add(new_instrument)
    db.commit()  # Commit the transaction to save the instrument in the database
    return new_instrument

def get_artist(db, artist_id: int):
    return db.query(Artist).filter(Artist.artist_id == artist_id).first()

def delete_artist(db, artist_id: int):
    artist = db.query(Artist).filter(Artist.artist_id == artist_id).first()
    if artist:
        db.delete(artist)
        db.commit()
    return artist

# Album operations

def create_album(db, sp_album_id: str, name: str, artist_id: int, cover: str):
    album = Album(sp_album_id=sp_album_id, name=name, artist_id=artist_id, cover=cover)
    db.add(album)
    db.commit()
    db.refresh(album)
    return album

def get_album(db, album_id: int):
    return db.query(Album).filter(Album.album_id == album_id).first()

def delete_album(db, album_id: int):
    album = db.query(Album).filter(Album.album_id == album_id).first()
    if album:
        db.delete(album)
        db.commit()
    return album

# Song operations

def create_song(db, title: str, spotify_song_id: str, artist_id: int, album_id: int, release_year: int, track_length: int):
    song = Song(title=title, spotify_song_id=spotify_song_id, artist_id=artist_id, album_id=album_id, release_year=release_year, track_length=track_length)
    db.add(song)
    db.commit()
    db.refresh(song)
    return song

def get_song(db, song_id: int):
    return db.query(Song).filter(Song.song_id == song_id).first()

def delete_song(db, song_id: int):
    song = db.query(Song).filter(Song.song_id == song_id).first()
    if song:
        db.delete(song)
        db.commit()
    return song

# Collection operations

def create_collection(db, user_id: int, song_id: int, name: str, description: str):
    collection = Collection(user_id=user_id, song_id=song_id, collection_name=name, collection_description=description)
    db.add(collection)
    db.commit()
    db.refresh(collection)
    return collection

def get_collection(db, collection_id: int):
    return db.query(Collection).filter(Collection.collection_id == collection_id).first()

def delete_collection(db, collection_id: int):
    collection = db.query(Collection).filter(Collection.collection_id == collection_id).first()
    if collection:
        db.delete(collection)
        db.commit()
    return collection

# Instrument operations

def create_instrument(db, name: str, colour: str):
    instrument = Instrument(name=name, colour=colour)
    db.add(instrument)
    db.commit()
    db.refresh(instrument)
    return instrument

def get_instrument(db, instrument_id: int):
    return db.query(Instrument).filter(Instrument.instrument_id == instrument_id).first()

def delete_instrument(db, instrument_id: int):
    instrument = db.query(Instrument).filter(Instrument.instrument_id == instrument_id).first()
    if instrument:
        db.delete(instrument)
        db.commit()
    return instrument

# Segment operations

def create_segment(db, collection_id: int, user_id: int, segment_name: str, start_time: int, end_time: int, segment_description: str, lead: bool):
    segment = Segment(collection_id=collection_id, user_id=user_id, segment_name=segment_name, start_time=start_time, end_time=end_time, segment_description=segment_description, lead=lead)
    db.add(segment)
    db.commit()
    db.refresh(segment)
    return segment

def get_segment(db, segment_id: int):
    return db.query(Segment).filter(Segment.segment_id == segment_id).first()

def update_segment(db, segment_id: int, new_data: dict):
    segment = db.query(Segment).filter(Segment.segment_id == segment_id).first()
    if segment:
        for key, value in new_data.items():
            setattr(segment, key, value)
        db.commit()
        db.refresh(segment)
    return segment

def delete_segment(db, segment_id: int):
    segment = db.query(Segment).filter(Segment.segment_id == segment_id).first()
    if segment:
        db.delete(segment)
        db.commit()
    return segment

# Section operations

def create_section(db, collection_id: int, section_name: str, start_time: int, end_time: int):
    section = Section(collection_id=collection_id, section_name=section_name, start_time=start_time, end_time=end_time)
    db.add(section)
    db.commit()
    db.refresh(section)
    return section

def get_section(db, section_id: int):
    return db.query(Section).filter(Section.section_id == section_id).first()

def delete_section(db, section_id: int):
    section = db.query(Section).filter(Section.section_id == section_id).first()
    if section:
        db.delete(section)
        db.commit()
    return section

# SegmentArtist operations

def create_segment_artist(db, segment_id: int, artist_id: int, instrument_id: int):
    segment_artist = SegmentArtist(segment_id=segment_id, artist_id=artist_id, instrument_id=instrument_id)
    db.add(segment_artist)
    db.commit()
    db.refresh(segment_artist)
    return segment_artist

def get_segment_artist(db, segment_id: int, artist_id: int):
    return db.query(SegmentArtist).filter(SegmentArtist.segment_id == segment_id, SegmentArtist.artist_id == artist_id).first()

def delete_segment_artist(db, segment_id: int, artist_id: int):
    segment_artist = db.query(SegmentArtist).filter(SegmentArtist.segment_id == segment_id, SegmentArtist.artist_id == artist_id).first()
    if segment_artist:
        db.delete(segment_artist)
        db.commit()
    return segment_artist

# Unchanged Operations

def get_spotify_user(db, spotify_user_id):
    return db.query(User).filter(User.spotify_user_id == spotify_user_id).first()

def get_session_user(db, session_id):
    return db.query(User).filter(User.session_id == session_id).first()

def get_spotify_song(db, spotify_song_id):
    return db.query(Song).filter(Song.spotify_song_id == spotify_song_id).first()

def get_artist_by_slug(db, slug):
    return db.query(Artist).filter(Artist.slug == slug).first()

def get_album_by_slug(db, slug):
    return db.query(Album).filter(Album.slug == slug).first()

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

def get_token(db, user_id):
    logging.info(f"Fetching token for user_id: {user_id}")
    token = db.query(Token).filter_by(user_id=user_id).first()
    if token:
        logging.info(f"Token found: {token}")
    else:
        logging.warning(f"No token found for user_id: {user_id}")
    return token