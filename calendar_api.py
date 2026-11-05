import os
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# full calendar access so it can make its own "Study Planner" calendar
SCOPES = ['https://www.googleapis.com/auth/calendar']
TIMEZONE = 'America/Vancouver'
tz = ZoneInfo(TIMEZONE)


def get_service():
    # login code from the google calendar python quickstart
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return build('calendar', 'v3', credentials=creds)


def get_planner_calendar(service):
    # the system only writes to this calendar so it never touches my real events
    calendars = service.calendarList().list().execute()
    for cal in calendars['items']:
        if cal['summary'] == 'Study Planner':
            return cal['id']
    new_cal = service.calendars().insert(body={'summary': 'Study Planner', 'timeZone': TIMEZONE}).execute()
    return new_cal['id']


def get_calendar_load(service, days=2, busy_hours=6):
    # adds up how many hours of events I have in the next 2 days
    # more than 6 hours = busy
    now = datetime.now(tz)
    end = now + timedelta(days=days)
    events = service.events().list(calendarId='primary', timeMin=now.isoformat(),
                                   timeMax=end.isoformat(), singleEvents=True).execute()

    hours = 0
    for event in events.get('items', []):
        if 'dateTime' not in event['start']:
            continue  # skip all day events like birthdays
        start = datetime.fromisoformat(event['start']['dateTime'])
        finish = datetime.fromisoformat(event['end']['dateTime'])
        hours = hours + (finish - start).total_seconds() / 3600

    print(f"Hours booked in the next {days} days: {hours:.1f}")
    if hours > busy_hours:
        return 'busy'
    return 'light'


def clear_today(service, cal_id):
    # remove anything the planner already put on today so it doesn't double book
    today = datetime.now(tz).replace(hour=0, minute=0, second=0, microsecond=0)
    events = service.events().list(calendarId=cal_id, timeMin=today.isoformat(),
                                   timeMax=(today + timedelta(days=1)).isoformat(),
                                   singleEvents=True).execute()
    for event in events.get('items', []):
        service.events().delete(calendarId=cal_id, eventId=event['id']).execute()


def schedule_action(service, action):
    cal_id = get_planner_calendar(service)
    clear_today(service, cal_id)

    # start at the next full hour
    start = datetime.now(tz).replace(minute=0, second=0, microsecond=0) + timedelta(hours=1)

    if action == 'intense':
        event = {'summary': 'Intense study block (mandatory)',
                 'start': {'dateTime': start.isoformat(), 'timeZone': TIMEZONE},
                 'end': {'dateTime': (start + timedelta(hours=5)).isoformat(), 'timeZone': TIMEZONE}}
    elif action == 'light':
        event = {'summary': 'Light review session',
                 'start': {'dateTime': start.isoformat(), 'timeZone': TIMEZONE},
                 'end': {'dateTime': (start + timedelta(hours=1)).isoformat(), 'timeZone': TIMEZONE}}
    else:
        today = datetime.now(tz).date()
        event = {'summary': 'Rest day',
                 'start': {'date': today.isoformat()},
                 'end': {'date': (today + timedelta(days=1)).isoformat()}}

    service.events().insert(calendarId=cal_id, body=event).execute()
    print("Added to calendar:", event['summary'])


if __name__ == '__main__':
    # quick test: log in, check how busy I am, add a light session
    service = get_service()
    print("Calendar load:", get_calendar_load(service))
    schedule_action(service, 'light')