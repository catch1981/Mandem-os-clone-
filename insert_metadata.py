import sqlite3
import json
import os
from setup_database import DB_NAME, setup_database

METADATA_FILE = 'metadata.json'

def insert_metadata():
    if not os.path.exists(DB_NAME):
        setup_database()

    with open(METADATA_FILE, 'r') as f:
        data = json.load(f)

    name = data.get('name')
    description = data.get('description')
    if not (name and description):
        raise ValueError('metadata.json missing name or description')

    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute(
        'INSERT INTO scrolls (name, description) VALUES (?, ?)',
        (name, description)
    )
    conn.commit()
    conn.close()
    print(f"Inserted '{name}' into scrolls table of {DB_NAME}.")

if __name__ == '__main__':
    insert_metadata()
