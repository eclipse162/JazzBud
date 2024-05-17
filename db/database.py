from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from pathlib import Path
from models.py import Base

# Define the database URL
DATABASE_URL = "postgres://jazzbuddy:FRpSvLa0sq0T4ifn6N3oC5ac1NPKt73V@dpg-cn5d2hv109ks739tk7h0-a.oregon-postgres.render.com/jazzbudb"

# Create the SQLAlchemy engine
engine = create_engine(DATABASE_URL)

# Bind the engine to the base class
Base.metadata.bind = engine

# Create a sessionmaker
Session = sessionmaker(bind=engine)

# Create a session
session = Session()

# Create the tables
Base.metadata.create_all(engine)

# Close the session
session.close()
