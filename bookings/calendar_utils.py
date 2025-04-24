# bookings/calendar_utils.py

import datetime
import os
from google.oauth2 import service_account
from googleapiclient.discovery import build

# Path to your service account key JSON
GOOGLE_CALENDAR_CREDENTIALS_FILE = os.path.join('path_to', 'credentials.json')

# Create a service account scope
SCOPES = ['https://www.googleapis.com/auth/calendar']

# Your Google Calendar ID (can be found in your Google Calendar settings)
CALENDAR_ID = 'e510f6bf8845ce1f7820a8ffbdfb9bf1ac8c61eb2edbb653823c3533609315ac@group.calendar.google.com'

def create_event(booking):
    creds = service_account.Credentials.from_service_account_file(
        GOOGLE_CALENDAR_CREDENTIALS_FILE, scopes=SCOPES)

    service = build('calendar', 'v3', credentials=creds)

    start_datetime = datetime.datetime.combine(booking.date, booking.time)
    end_datetime = start_datetime + datetime.timedelta(minutes=booking.service.duration_minutes or 60)

    event = {
        'summary': f'Appointment with {booking.name}',
        'location': 'Your Business Location',
        'description': f'Service: {booking.service.name}\nClient: {booking.email}\nPhone: {booking.phone}',
        'start': {
            'dateTime': start_datetime.isoformat(),
            'timeZone': 'Africa/Lagos',  # Set your timezone
        },
        'end': {
            'dateTime': end_datetime.isoformat(),
            'timeZone': 'Africa/Lagos',
        },
        'attendees': [
            {'email': booking.email},
            {'email': 'admin@example.com'},
        ],
        'reminders': {
            'useDefault': True,
        },
    }

    created_event = service.events().insert(calendarId=CALENDAR_ID, body=event, sendUpdates="all").execute()
    return created_event
