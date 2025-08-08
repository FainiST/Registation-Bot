import sqlite3
from pathlib import Path

DB = Path(__file__).parent / "registrs.db"

def init_db():
    with sqlite3.connect(DB) as conn:
        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS registrations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phone TEXT NOT NULL,
            usrname TEXT,
        )
        """)

        conn.commit()

def add_registration(name: str, phone: str, usrname: str):
    with sqlite3.connect(DB) as conn:
        cursor = conn.cursor()
        cursor.execute("""
        INSERT INTO registrations (name, phone, usrname)
        VALUES (?, ?, ?, ?)
        """, (name, phone, usrname))
        conn.commit()