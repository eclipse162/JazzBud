import json
from .crud import create_instrument
from .database import get_db

def insert_instruments():
    # Load JSON data
    with open("db/instruments.json", "r", encoding="utf-8") as file:
        data = json.load(file)

    db = get_db()

    # Insert instruments
    for instrument_id, name in data.items():
        create_instrument(db, name)

    print("Instruments inserted successfully!")