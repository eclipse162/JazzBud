from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from pathlib import Path

# Define the database URL
DATABASE_URL = "postgres://jazzbuddy:FRpSvLa0sq0T4ifn6N3oC5ac1NPKt73V@dpg-cn5d2hv109ks739tk7h0-a.oregon-postgres.render.com/jazzbudb"

# Create the SQLAlchemy engine
engine = create_engine(DATABASE_URL)

# Define a sessionmaker to interact with the database
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Define a context manager for managing database sessions
class DatabaseConnection:
    def __enter__(self):
        self.db = SessionLocal()
        return self.db

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.db:
            self.db.close()

# Define the models for the database
from .models import Base, User, Song, Segment

# Initialize database tables
Base.metadata.create_all(bind=engine)