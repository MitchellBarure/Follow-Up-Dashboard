"""
sheets_client.py
This file handles all the google sheet logic by:
1. logining into google sheet api using my service_account.json,
2. and using the API to read and update records on the google sheet.
"""

import os
import datetime
from google.oauth2 import service_account
from googleapiclient.discovery import build

#CCONFIGURE THE GOOGLE SHEET
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SERVICE_ACCOUNT_FILE = os.path.join(BASE_DIR, "service_account.json") #path to my json key

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
SPREADSHEET_ID = "1RYbqgjW8msK3_40748N8l6C2FNSrcY7a_VAi_kdec2g"
RANGE = "Sheet1!A2:H" #Possibly edit later

#CONNECT TO THE GOOGLE SHEET
def get_service():
    creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE,
        scopes=SCOPES
    )
    return build("sheets", "v4", credentials=creds)

#READ RECORDS
def read_records():
    service = get_service()
    sheet = service.spreadsheets()

    result = sheet.values().get(
        spreadsheetId=SPREADSHEET_ID,
        range=RANGE
    ).execute()

    values = result.get('values', [])

    records = []
    #Append data from Google sheet into a dictionary
    for row in values:
        while len(row) < 8:
            row.append("")

        records.append({
            "id": row[0],
            "Name": row[1],
            "Phone": row[2],
            "Category": row[3],
            "Status": row[4],
            "AssignedTo": row[5],
            "LastUpdated": row[6],
            "Notes": row[7],
        })

    return records

#UPDATE RECORDS (when a user modifies a record, update the status, notes and timestamP)
def update_record(record_id, new_status, new_notes):
    service = get_service()
    sheet = service.spreadsheets()

    #Fetch all rows to find the correct row index
    all_records = read_records()

    row_index = None
    for i, r in enumerate(all_records):
        if r["id"] == record_id:
            row_index = i + 2
            break

    if row_index is None:
        return False

    now = datetime.datetime.now(datetime.timezone.utc).isoformat()

    updated_row = [
        record_id,
        all_records[row_index - 2]["Name"],
        all_records[row_index - 2]["Phone"],
        all_records[row_index - 2]["Category"],
        new_status,
        all_records[row_index - 2]["AssignedTo"],
        now,
        new_notes
    ]

    #Write back the updates to google sheets
    range_to_update = f"Sheet1!A{row_index}:H{row_index}"

    request = sheet.values().update(
        spreadsheetId=SPREADSHEET_ID,
        range=range_to_update,
        valueInputOption="USER_ENTERED",
        body={"values": [updated_row]},
    )

    request.execute()
    return True

