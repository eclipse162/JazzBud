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
    sp_artist_id = Column(String(255))
    name = Column(String(100), nullable=False)
    cover = Column(String(255))
    albums = relationship("Album", back_populates="artist")
    songs = relationship("Song", back_populates="artist")

class Album(Base):
    __tablename__ = 'albums'

    album_id = Column(Integer, primary_key=True, autoincrement=True)
    sp_album_id = Column(String(255))
    name = Column(String(255), nullable=False)
    artist = relationship("Artist", back_populates="albums")
    artist_id = Column(Integer, ForeignKey('artists.artist_id'), nullable=False)
    cover = Column(String(255))
    songs = relationship("Song", back_populates="album")
class Song(Base):
    __tablename__ = 'songs'
    
    song_id = Column(Integer, primary_key=True, autoincrement=True)
    sp_song_id = Column(String(255))
    title = Column(String(255), nullable=False)
    artist_id = Column(Integer, ForeignKey('artists.artist_id'), nullable=False)
    album_id = Column(Integer, ForeignKey('albums.album_id'), nullable=False)
    artist = relationship("Artist", back_populates="songs")
    album = relationship("Album", back_populates="songs")
    cover = Column(String(255))
    release_year = Column(Integer)
    track_length = Column(Integer)
    collections = relationship("Collection", back_populates="song")

class Collection(Base):
    __tablename__ = 'collections'
    collection_id = Column(Integer, primary_key=True, autoincrement=True)
    song_id = Column(Integer, ForeignKey('songs.song_id'), nullable=False)
    collection_name = Column(String(50))
    collection_description = Column(Text)
    song = relationship("Song", back_populates="collections")
    segments = relationship("Segment", back_populates="collection")

class Segment(Base):
    __tablename__ = 'segments'
    
    segment_id = Column(Integer, primary_key=True, autoincrement=True)
    collection_id = Column(Integer, ForeignKey('collections.collection_id'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    segment_name = Column(String(50))
    start_time = Column(Integer)
    end_time = Column(Integer)
    segment_description = Column(Text)
    collection = relationship("Collection", back_populates="segments")
    user = relationship("User", back_populates="segments")

# def generate_unique_slug(mapper, connection, target):
#     if isinstance(target, Artist) and not target.slug:
#         base_slug = slugify(target.name)
#         slug = base_slug
#         counter = 1
#         while connection.execute(f"SELECT 1 FROM artists WHERE slug='{slug}'").fetchone():
#             slug = f"{base_slug}-{counter}"
#             counter += 1
#         target.slug = slug

#     if isinstance(target, Album) and not target.slug:
#         base_slug = slugify(target.title)
#         slug = base_slug
#         counter = 1
#         while connection.execute(f"SELECT 1 FROM albums WHERE slug='{slug}' AND artist_id='{target.artist_id}'").fetchone():
#             slug = f"{base_slug}-{counter}"
#             counter += 1
#         target.slug = slug

# event.listen(Artist, 'before_insert', generate_unique_slug)
# event.listen(Album, 'before_insert', generate_unique_slug)

# event.listen(Artist, 'before_update', generate_unique_slug)
# event.listen(Album, 'before_update', generate_unique_slug)