from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from django.utils import timezone

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False)
    spotify_user_id = Column(String(255), unique=True)
    is_authenticated = Column(Boolean, default=False)
    display_name = Column(String(50))
    session_id = Column(String(255))

    token = relationship("Token", uselist=False, back_populates="user")
    segments = relationship("Segment", back_populates="user")

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

class Song(Base):
    __tablename__ = 'songs'

    song_id = Column(Integer, primary_key=True, autoincrement=True)
    spotify_song_id = Column(String(255))
    title = Column(String(255), nullable=False)
    artist = Column(String(100))
    album = Column(String(100))
    genre = Column(String(50))
    release_year = Column(Integer)
    segments = relationship("Segment", back_populates="song")

class Segment(Base):
    __tablename__ = 'segments'

    segment_id = Column(Integer, primary_key=True, autoincrement=True)
    song_id = Column(Integer, ForeignKey('songs.song_id'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    segment_name = Column(String(50))
    start_time = Column(Integer)
    end_time = Column(Integer)
    segment_description = Column(Text)
    song = relationship("Song", back_populates="segments")
    user = relationship("User", back_populates="segments")
