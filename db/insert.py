import json
from .crud import create_instrument
from .database import get_db

def insert_instruments():
    # Load JSON data
    with open("db/instruments.json", "r", encoding="utf-8") as file:
        data = json.load(file)

    # Insert instruments
    with get_db() as db:
        for instrument_id, name in data.items():
            create_instrument(db, name)

    print("Instruments inserted successfully!")