"""
test_sheets.py
This script serves as a tester for the Google sheets API:
1. Tests if there was a successful connection to Google sheets using my service account
2. Checks if a record can be successfully added to the Google sheet
"""

from sheets_client import get_service, read_records, SPREADSHEET_ID
import datetime

def add_test_record():
    service = get_service()
    sheet = service.spreadsheets()
    now = datetime.datetime.now(datetime.timezone.utc).isoformat()
    # id, Name, Phone, Category, Status, AssignedTo, LastUpdated, Notes
    new_row = [
        "01", "Test User", "+250795986428", "FIRST_TIMER", "NOT_CONTACTED", "Successful", now, "Created via API"
    ]
    request = sheet.values().append(
        spreadsheetId=SPREADSHEET_ID,
        range="Sheet1!A:H",
        valueInputOption="USER_ENTERED",
        body={"values": [new_row]},
    )
    response = request.execute()
    print("Record added:", response)

if __name__ == '__main__':
    add_test_record()
    records = read_records()
    print("Records:", records)
