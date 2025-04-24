import gspread
from oauth2client.service_account import ServiceAccountCredentials

def test_google_connection():
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]
    creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
    client = gspread.authorize(creds)

    # Test: Fetch spreadsheet list (this will confirm it's working)
    try:
        sheet_list = client.openall()
        print("✅ Connection successful! Found these spreadsheets:")
        for sheet in sheet_list:
            print(f" - {sheet.title}")
    except Exception as e:
        print("❌ Error connecting to Google Sheets:", e)

if __name__ == "__main__":
    test_google_connection()
