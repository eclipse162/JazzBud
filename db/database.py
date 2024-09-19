import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager

# Database URL
# DATABASE_URL = os.getenv('DATABASE_URL')
DATABASE_URL = "postgresql://jazzbuddy:FRpSvLa0sq0T4ifn6N3oC5ac1NPKt73V@dpg-cn5d2hv109ks739tk7h0-a.oregon-postgres.render.com/jazzbudb"

# Create the database engine
engine = create_engine(DATABASE_URL, echo=True)

# Create a configured "Session" class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a Base class for our models to inherit from
Base = declarative_base()

# Dependency to get the session
@contextmanager
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()