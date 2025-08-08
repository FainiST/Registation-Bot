import time
import sqlite3
from pathlib import Path
import gspread
from google.oauth2.service_account import Credentials

TAB_NAME = "registrations"
BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "database" / "registrs.db"

SHEET_ID = '1Qpm2cakUmtEqe4g7AI6U4S1tb2AyLCkRCBZ3cdYPgXc'
SHEET_NAME = 'Sheet1'

SCOPES = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
CREDS_FILE = Path(__file__).resolve().parent / 'cred.json'

def get_data_from_db():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT name, phone, usrname FROM registrations")
        return cursor.fetchall()

def update_google_sheet(data):
    creds = Credentials.from_service_account_file(str(CREDS_FILE), scopes=SCOPES)
    client = gspread.authorize(creds)
    sheet = client.open_by_key(SHEET_ID).worksheet(SHEET_NAME)
    sheet.clear()
    sheet.append_row(['name', 'phone', 'usrname'])
    if data:
        sheet.append_rows(data)

def main():
    while True:
        data = get_data_from_db()
        update_google_sheet(data)
        time.sleep(600)

if __name__ == "__main__":
    main()
