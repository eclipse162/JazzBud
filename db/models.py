from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True)
    spotify_user_id = Column(String(255))
    username = Column(String(50), unique=True, nullable=False)
    segments = relationship("Segment", back_populates="user")

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
