import time
import sqlite3
from pathlib import Path
import gspread
from google.oauth2.service_account import Credentials

BASE_DIR = Path(__file__).resolve().parent.parent
DB = BASE_DIR / "database" / "registrs.db"
TAB_NAME = "registrations"

SHEET_ID = '1Qpm2cakUmtEqe4g7AI6U4S1tb2AyLCkRCBZ3cdYPgXc'
SHEET_NAME = '1'

SCOPES = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
CREDS_FILE = 'cred.json'

def get_data_from_db():
    conn = sqlite3.connect('../database/registrs.db')
    cursor = conn.cursor()
    cursor.execute("SELECT name, phone, usrname FROM registrations")
    data = cursor.fetchall()
    conn.close()
    return data

def update_google_sheet(data):
    creds = Credentials.from_service_account_file(CREDS_FILE, scopes=SCOPES)
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
        time.sleep(600)  #10 минуток

if __name__ == "__main__":
    main()
