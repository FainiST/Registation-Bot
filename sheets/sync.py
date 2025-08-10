import time
import sqlite3
import logging
from pathlib import Path

import gspread
from google.oauth2.service_account import Credentials

from database.db import DB as DB_PATH

SHEET_ID = '1Qpm2cakUmtEqe4g7AI6U4S1tb2AyLCkRCBZ3cdYPgXc'
SHEET_NAME = 'Sheet1'

SCOPES = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
CREDS_FILE = Path(__file__).resolve().parent / 'cred.json'

HEADER = ['name', 'phone', 'usrname']

logger = logging.getLogger(__name__)


def get_data_from_db():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT name, phone, usrname FROM registrations ORDER BY id ASC")
        return cursor.fetchall()


def ensure_header_and_get_current_count(sheet):
    values = sheet.get_all_values()
    if not values:
        sheet.update('A1:C1', [HEADER])
        return 0

    header = values[0]
    if header != HEADER:
        sheet.update('A1:C1', [HEADER])
    return max(len(values) - 1, 0)


def update_google_sheet_incremental(data):
    creds = Credentials.from_service_account_file(str(CREDS_FILE), scopes=SCOPES)
    client = gspread.authorize(creds)
    sheet = client.open_by_key(SHEET_ID).worksheet(SHEET_NAME)

    current_rows = ensure_header_and_get_current_count(sheet)

    rows_to_append = data[current_rows:]
    if rows_to_append:
        sheet.append_rows(rows_to_append)
    else:
        print()


def main():
    while True:
        try:
            data = get_data_from_db()
            update_google_sheet_incremental(data)
        except Exception as exc:
            logger.exception("Ошибка при синхронизации с Google Sheets: %s", exc)
        time.sleep(350)

if __name__ == "__main__":
    main()
