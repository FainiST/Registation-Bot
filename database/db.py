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
            chat_id INTEGER NOT NULL
        )
        """)

        conn.commit()

def add_registration(name: str, phone: str, usrname: str, chat_id: int):
    with sqlite3.connect(DB) as conn:
        cursor = conn.cursor()
        cursor.execute("""
        INSERT INTO registrations (name, phone, usrname, chat_id)
        VALUES (?, ?, ?, ?)
        """, (name, phone, usrname, chat_id))
        conn.commit()