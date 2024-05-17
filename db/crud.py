from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from models.py import Base, User, Song, Segment, UserSegment

# Create SQLAlchemy engine
DATABASE_URL = "postgres://jazzbuddy:FRpSvLa0sq0T4ifn6N3oC5ac1NPKt73V@dpg-cn5d2hv109ks739tk7h0-a.oregon-postgres.render.com/jazzbudb"
engine = create_engine(DATABASE_URL)

# Create base class for declarative class definitions
Base = declarative_base()

# CRUD operations for users
def create_user(spotify_user_id, username):
    user = User(spotify_user_id=spotify_user_id, username=username)
    session.add(user)
    session.commit()
    return user

def get_user_by_id(user_id):
    return session.query(User).filter(User.user_id == user_id).first()

def get_user_by_username(username):
    return session.query(User).filter(User.username == username).first()

def update_username(user_id, new_username):
    user = session.query(User).filter(User.user_id == user_id).first()
    if user:
        user.username = new_username
        session.commit()
        return user
    return None

# CRUD operations for songs
def create_song(spotify_song_id, title, artist, album, genre, release_year):
    song = Song(spotify_song_id=spotify_song_id, title=title, artist=artist, album=album,
                genre=genre, release_year=release_year)
    session.add(song)
    session.commit()
    return song

def get_song_by_id(song_id):
    return session.query(Song).filter(Song.song_id == song_id).first()

# CRUD operations for segments
def create_segment(song_id, segment_name, start_time, end_time, segment_description=None):
    segment = Segment(song_id=song_id, segment_name=segment_name, start_time=start_time,
                      end_time=end_time, segment_description=segment_description)
    session.add(segment)
    session.commit()
    return segment

def get_segment_by_id(segment_id):
    return session.query(Segment).filter(Segment.segment_id == segment_id).first()

# CRUD operations for user segments
def create_user_segment(user_id, song_id, segment_id):
    user_segment = UserSegment(user_id=user_id, song_id=song_id, segment_id=segment_id)
    session.add(user_segment)
    session.commit()
    return user_segment

def get_user_segments(user_id, song_id):
    return session.query(UserSegment).filter(UserSegment.user_id == user_id, UserSegment.song_id == song_id).all()

# Example usage:
if __name__ == "__main__":
    # Create a new user
    user = create_user(spotify_user_id='spotify123', username='example_user')

    # Update user's username
    updated_user = update_username(user_id=user.user_id, new_username='new_username')

    # Create a new song
    song = create_song(spotify_song_id='spotify:123', title='Example Song', artist='Example Artist', album='Example Album', genre='Example Genre', release_year=2024)

    # Create a new segment associated with the song
    segment = create_segment(song_id=song.song_id, segment_name='Verse', start_time=30, end_time=60, segment_description='Example verse')

    # Create a user segment associated with the user and song
    user_segment = create_user_segment(user_id=user.user_id, song_id=song.song_id, segment_id=segment.segment_id)

    # Retrieve user segments for a specific user and song
    user_segments = get_user_segments(user_id=user.user_id, song_id=song.song_id)
    for user_segment in user_segments:
        print("User Segment:", user_segment.segment.segment_name)
