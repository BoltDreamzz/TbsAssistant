import datetime
from google.oauth2 import service_account
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/calendar']
SERVICE_ACCOUNT_FILE = 'credentials.json'  # Place in project root

def add_to_calendar(booking):
    creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)

    service = build('calendar', 'v3', credentials=creds)

    event = {
        'summary': f"{booking.service.name} with {booking.name}",
        'description': f"Phone: {booking.phone}\nEmail: {booking.email}",
        'start': {
            'dateTime': datetime.datetime.combine(booking.date, booking.time).isoformat(),
            'timeZone': 'Africa/Lagos',
        },
        'end': {
            'dateTime': (datetime.datetime.combine(booking.date, booking.time) + datetime.timedelta(hours=1)).isoformat(),
            'timeZone': 'Africa/Lagos',
        },
    }

    event = service.events().insert(calendarId='primary', body=event).execute()
    print(f"Event created: {event.get('htmlLink')}")
