from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
import datetime

Base = declarative_base()

class Token(Base):
    __tablename__ = 'tokens'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    access_token = Column(String(500))
    refresh_token = Column(String(500))
    expires_in = Column(DateTime)
    token_type = Column(String(100))

    user = relationship("User", back_populates="token")

    def __repr__(self):
        return f"<Token(user_id='{self.user_id}', access_token='{self.access_token}')>"

class User(Base):
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True)
    spotify_user_id = Column(String(255))
    username = Column(String(50), unique=True, nullable=False)
    segments = relationship("Segment", back_populates="user")
    token = relationship("Token", uselist=False, back_populates="user")

class Song(Base):
    __tablename__ = 'songs'

    song_id = Column(Integer, primary_key=True)
    spotify_song_id = Column(String(255))
    title = Column(String(255), nullable=False)
    artist = Column(String(100))
    album = Column(String(100))
    genre = Column(String(50))
    release_year = Column(Integer)
    segments = relationship("Segment", back_populates="song")

class Segment(Base):
    __tablename__ = 'segments'

    segment_id = Column(Integer, primary_key=True)
    song_id = Column(Integer, ForeignKey('songs.song_id'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    segment_name = Column(String(50))
    start_time = Column(Integer)
    end_time = Column(Integer)
    segment_description = Column(Text)
    song = relationship("Song", back_populates="segments")
    user = relationship("User", back_populates="segments")
