import os
import time
import sqlite3
import logging
from pathlib import Path

import gspread
from google.oauth2.service_account import Credentials

from database.db import DB as DB_PATH

SHEET_ID = os.getenv('GSHEET_ID', '')
SHEET_NAME = os.getenv('GSHEET_DATA_SHEET', 'Sheet1')

META_SHEET_NAME = os.getenv('GSHEET_META_SHEET', 'meta')

SCOPES = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']

DEFAULT_CREDS_FILE = Path(__file__).resolve().parent.parent / '.secrets' / 'cred.json'

HEADER = ['name', 'phone', 'usrname']

logger = logging.getLogger(__name__)


def get_data_from_db():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT name, phone, usrname FROM registrations ORDER BY id ASC")
        return cursor.fetchall()


def ensure_sheets_and_get_last_synced(client):
    spreadsheet = client.open_by_key(SHEET_ID)
    sheet_titles = [ws.title for ws in spreadsheet.worksheets()]

    if SHEET_NAME not in sheet_titles:
        spreadsheet.add_worksheet(title=SHEET_NAME, rows=1000, cols=3)
    data_sheet = spreadsheet.worksheet(SHEET_NAME)

    values = data_sheet.get_all_values()
    if not values:
        data_sheet.update('A1:C1', [HEADER])
    elif values[0] != HEADER:
        data_sheet.update('A1:C1', [HEADER])

    if META_SHEET_NAME not in sheet_titles:
        spreadsheet.add_worksheet(title=META_SHEET_NAME, rows=10, cols=2)
    meta_sheet = spreadsheet.worksheet(META_SHEET_NAME)

    # last_synced_id храним в ячейке A1
    meta_values = meta_sheet.get('A1')
    last_synced_id = 0
    if meta_values and meta_values[0] and len(meta_values[0]) > 0:
        try:
            last_synced_id = int(meta_values[0][0])
        except ValueError:
            last_synced_id = 0

    return data_sheet, meta_sheet, last_synced_id


def _build_credentials():
    env_keys = {
        'type': os.getenv('GOOGLE_TYPE'),
        'project_id': os.getenv('GOOGLE_PROJECT_ID'),
        'private_key_id': os.getenv('GOOGLE_PRIVATE_KEY_ID'),
        'private_key': os.getenv('GOOGLE_PRIVATE_KEY'),
        'client_email': os.getenv('GOOGLE_CLIENT_EMAIL'),
        'client_id': os.getenv('GOOGLE_CLIENT_ID'),
        'auth_uri': os.getenv('GOOGLE_AUTH_URI'),
        'token_uri': os.getenv('GOOGLE_TOKEN_URI'),
        'auth_provider_x509_cert_url': os.getenv('GOOGLE_AUTH_PROVIDER_X509_CERT_URL'),
        'client_x509_cert_url': os.getenv('GOOGLE_CLIENT_X509_CERT_URL'),
        'universe_domain': os.getenv('GOOGLE_UNIVERSE_DOMAIN', 'googleapis.com'),
    }
    if all(env_keys.values()):
        return Credentials.from_service_account_info(env_keys, scopes=SCOPES)

    if DEFAULT_CREDS_FILE.exists():
        return Credentials.from_service_account_file(str(DEFAULT_CREDS_FILE), scopes=SCOPES)

    legacy_file = Path(__file__).resolve().parent / 'cred.json'
    if legacy_file.exists():
        return Credentials.from_service_account_file(str(legacy_file), scopes=SCOPES)

    raise RuntimeError('1')


def update_google_sheet_incremental():
    creds = _build_credentials()
    client = gspread.authorize(creds)

    data_sheet, meta_sheet, last_synced_id = ensure_sheets_and_get_last_synced(client)

    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, name, phone, usrname FROM registrations WHERE id > ? ORDER BY id ASC",
            (last_synced_id,)
        )
        new_rows = cursor.fetchall()

    if not new_rows:
        logger.debug('Новых записей для синхронизации нет')
        return

    payload = [[name, phone, usrname] for (_id, name, phone, usrname) in new_rows]
    data_sheet.append_rows(payload)

    new_last_id = new_rows[-1][0]
    meta_sheet.update('A1', [[str(new_last_id)]])
    logger.info('Синхронизировано новых записей: %s, last_synced_id=%s', len(new_rows), new_last_id)


def main():
    while True:
        try:
            update_google_sheet_incremental()
        except Exception as exc:
            logger.exception("Ошибка при синхронизации с Google Sheets: %s", exc)
        time.sleep(350)

if __name__ == "__main__":
    main()
