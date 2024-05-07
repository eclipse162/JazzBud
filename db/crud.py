from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

# Create SQLAlchemy engine
DATABASE_URL = "postgres://jazzbuddy:FRpSvLa0sq0T4ifn6N3oC5ac1NPKt73V@dpg-cn5d2hv109ks739tk7h0-a.oregon-postgres.render.com/jazzbudb"
engine = create_engine(DATABASE_URL)

# Create base class for declarative class definitions
Base = declarative_base()

# Define User class for the users table
class User(Base):
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True)
    spotify_user_id = Column(String(255))
    username = Column(String(50), unique=True, nullable=False)

# Define Song class for the songs table
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

# Define Segment class for the segments table
class Segment(Base):
    __tablename__ = 'segments'

    segment_id = Column(Integer, primary_key=True)
    song_id = Column(Integer, ForeignKey('songs.song_id'))
    segment_name = Column(String(50))
    start_time = Column(Integer)
    end_time = Column(Integer)
    segment_description = Column(Text)
    song = relationship("Song", back_populates="segments")

# Create tables in the database
Base.metadata.create_all(engine)

# Create a sessionmaker to interact with the database
Session = sessionmaker(bind=engine)
session = Session()

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

    # Retrieve a user by their ID
    retrieved_user = get_user_by_id(user_id=user.user_id)
    print("Retrieved User:", retrieved_user.username)

    # Retrieve a song by its ID
    retrieved_song = get_song_by_id(song_id=song.song_id)
    print("Retrieved Song:", retrieved_song.title)

    # Retrieve a segment by its ID
    retrieved_segment = get_segment_by_id(segment_id=segment.segment_id)
    print("Retrieved Segment:", retrieved_segment.segment_name)