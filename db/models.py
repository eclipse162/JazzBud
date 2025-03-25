from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, Boolean, event
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from django.utils import timezone
from slugify import slugify

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True, autoincrement=True)
    session_id = Column(String(50))
    username = Column(String(50), unique=True, nullable=False)
    spotify_user_id = Column(String(255), unique=True)
    is_authenticated = Column(Boolean, default=False)
    display_name = Column(String(50))

    token = relationship("Token", uselist=False, back_populates="user")
    segments = relationship("Segment", back_populates="user")
    collections = relationship("Collection", back_populates="user")

class Token(Base):
    __tablename__ = 'tokens'

    token_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    created_at = Column(DateTime, default=timezone.now)
    access_token = Column(String(500))
    refresh_token = Column(String(500))
    expires_in = Column(DateTime)
    token_type = Column(String(100))

    user = relationship("User", back_populates="token")

class Artist(Base):
    __tablename__ = 'artists'

    artist_id = Column(Integer, primary_key=True, autoincrement=True)
    sp_artist_id = Column(String(255), unique=True)
    name = Column(String(100), nullable=False, index=True)
    cover = Column(String(255))

    albums = relationship("Album", back_populates="artist")
    songs = relationship("Song", back_populates="artist")
    segment_artists = relationship("SegmentArtist", back_populates="artist")

class Album(Base):
    __tablename__ = 'albums'

    album_id = Column(Integer, primary_key=True, autoincrement=True)
    sp_album_id = Column(String(255), unique=True)
    name = Column(String(255), nullable=False, index=True)
    artist_id = Column(Integer, ForeignKey('artists.artist_id', ondelete='CASCADE'), nullable=False)
    cover = Column(String(255))

    artist = relationship("Artist", back_populates="albums")
    songs = relationship("Song", back_populates="album")

class Song(Base):
    __tablename__ = 'songs'

    song_id = Column(Integer, primary_key=True, autoincrement=True)
    spotify_song_id = Column(String(255), unique=True)
    title = Column(String(255), nullable=False, index=True)
    artist_id = Column(Integer, ForeignKey('artists.artist_id', ondelete='CASCADE'), nullable=False)
    album_id = Column(Integer, ForeignKey('albums.album_id', ondelete='CASCADE'), nullable=False)
    release_year = Column(Integer)
    track_length = Column(Integer)

    artist = relationship("Artist", back_populates="songs")
    album = relationship("Album", back_populates="songs")
    collections = relationship("Collection", back_populates="song")

class Collection(Base):
    __tablename__ = 'collections'

    collection_id = Column(Integer, primary_key=True, autoincrement=True)
    song_id = Column(Integer, ForeignKey('songs.song_id', ondelete='CASCADE'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False)
    collection_name = Column(String(50), nullable=False)
    collection_description = Column(Text)

    song = relationship("Song", back_populates="collections")
    user = relationship("User", back_populates="collections")
    segments = relationship("Segment", back_populates="collection")
    sections = relationship("Section", back_populates="collection", cascade="all, delete-orphan")


class Segment(Base):
    __tablename__ = 'segments'

    segment_id = Column(Integer, primary_key=True, autoincrement=True)
    collection_id = Column(Integer, ForeignKey('collections.collection_id', ondelete='CASCADE'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False)
    segment_name = Column(String(50), nullable=False, index=True)
    start_time = Column(Integer, nullable=False)  # Start time in seconds
    end_time = Column(Integer, nullable=False)    # End time in seconds
    segment_description = Column(Text)
    lead = Column(Boolean, default=False)

    collection = relationship("Collection", back_populates="segments")
    user = relationship("User", back_populates="segments")
    segment_artists = relationship("SegmentArtist", back_populates="segment")

class SegmentArtist(Base):
    __tablename__ = 'segment_artists'

    segment_id = Column(Integer, ForeignKey('segments.segment_id', ondelete='CASCADE'), primary_key=True)
    artist_id = Column(Integer, ForeignKey('artists.artist_id', ondelete='CASCADE'), primary_key=True)
    instrument_id = Column(Integer, ForeignKey('instruments.instrument_id', ondelete='SET NULL'))

    segment = relationship("Segment", back_populates="segment_artists")
    artist = relationship("Artist", back_populates="segment_artists")
    instrument = relationship("Instrument")

class Instrument(Base):
    __tablename__ = 'instruments'

    instrument_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False, unique=True, index=True)
    colour = Column(String(255), nullable=False, unique=True, index=True)

class Section(Base):
    __tablename__ = 'sections'

    section_id = Column(Integer, primary_key=True, autoincrement=True)
    collection_id = Column(Integer, ForeignKey('collections.collection_id', ondelete='CASCADE'), nullable=False)
    section_name = Column(String(50), nullable=False, index=True)
    start_time = Column(Integer, nullable=False)
    end_time = Column(Integer, nullable=False)

    collection = relationship("Collection", back_populates="sections")
