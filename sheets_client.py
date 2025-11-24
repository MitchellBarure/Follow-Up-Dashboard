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
            "AssignedTo": row[3],
            "Category": row[4],
            "Status": row[5],
            "LastUpdated": row[6],
            "Notes": row[7],
        })

    return records

"""Control user input for AssignedTo Category, and Status.
ALLOWED_AssignedTo = [
    "Mitchell",
    "Raissa",
    "Mufaro",
    "Blen",
    "Lucia"
]

ALLOWED_CATEGORIES = [
    "ABSENT_FOR_A_WHILE",
    "FIRST_TIMER",
    "OUTREACH",
    "SECOND_TIMER"
]"""

ALLOWED_STATUSES = [
    "Waiting for a response",
    "No response",
    "Indecisive",
    "Available",
    "Unavailable"
]

#UPDATE RECORDS (when a user modifies a record, update the status, notes and timestamP)
def update_record(record_id, new_status, new_notes):
    service = get_service()
    sheet = service.spreadsheets()

    #Fetch all the rows to find the correct row index
    all_records = read_records()

    row_index = None
    for i, r in enumerate(all_records):
        if r["id"] == record_id:
            row_index = i + 2
            break

    if row_index is None:
        return False

    now = datetime.datetime.now(datetime.timezone.utc).isoformat()

    #Validate Status update
    if new_status not in ALLOWED_STATUSES:
        raise ValueError(f"Invalid status value: {new_status}")

    #Ensure that notes are always a string
    if new_notes is None:
        new_notes = ""

    updated_row = [
        record_id,
        all_records[row_index - 2]["Name"],
        all_records[row_index - 2]["Phone"],
        all_records[row_index - 2]["AssignedTo"],
        all_records[row_index - 2]["Category"],
        new_status,
        now,
        new_notes
    ]

    #Write back the updates to the Google sheet
    range_to_update = f"Sheet1!A{row_index}:H{row_index}"

    request = sheet.values().update(
        spreadsheetId=SPREADSHEET_ID,
        range=range_to_update,
        valueInputOption="USER_ENTERED",
        body={"values": [updated_row]},
    )

    request.execute()
    return True

def add_record(name, phone, assignedTo, category, status, notes=""):
    service = get_service()
    sheet = service.spreadsheets()

    all_records = read_records()

    # Determine next ID for new record additions
    if all_records:
        existing_ids = [int(r["id"]) for r in all_records if r["id"].isdigit()]
        next_id = str(max(existing_ids) + 1) if existing_ids else "1"
    else:
        next_id = "1"

    if status not in ALLOWED_STATUSES:
        raise ValueError(f"Invalid status value: {status}")

    if notes is None:
        notes = ""

    now = datetime.datetime.now(datetime.timezone.utc).isoformat()

    new_row = [
        next_id,
        name,
        phone,
        assignedTo,
        category,
        status,
        now,
        notes
    ]

    request = sheet.values().append(
        spreadsheetId=SPREADSHEET_ID,
        range="Sheet1!A:H",
        valueInputOption="USER_ENTERED",
        insertDataOption="INSERT_ROWS",
        body={"values": [new_row]},
    )

    request.execute()
    return next_id




