import os
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

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
    # only write to a separate calendar so my real events never get touched
    calendars = service.calendarList().list().execute()
    for cal in calendars['items']:
        if cal['summary'] == 'Study Planner':
            return cal['id']
    new_cal = service.calendars().insert(body={'summary': 'Study Planner', 'timeZone': TIMEZONE}).execute()
    return new_cal['id']


def clear_today(service, cal_id):
    # remove anything already planned for today so it doesn't double book
    today = datetime.now(tz).replace(hour=0, minute=0, second=0, microsecond=0)
    events = service.events().list(calendarId=cal_id, timeMin=today.isoformat(),
                                   timeMax=(today + timedelta(days=1)).isoformat()).execute()
    for event in events.get('items', []):
        service.events().delete(calendarId=cal_id, eventId=event['id']).execute()


def schedule_action(service, action, focus=None):
    cal_id = get_planner_calendar(service)
    clear_today(service, cal_id)

    if action == 'rest':
        today = datetime.now(tz).date()
        event = {'summary': 'Rest day',
                 'start': {'date': today.isoformat()},
                 'end': {'date': (today + timedelta(days=1)).isoformat()}}
    else:
        hours = {'intense': 5, 'practice': 2, 'light': 1}
        names = {'intense': 'Intense study block', 'practice': 'Practice problems', 'light': 'Light review'}
        title = names[action]
        if focus:
            title = title + ': focus on ' + focus

        # start at the next full hour
        start = datetime.now(tz).replace(minute=0, second=0, microsecond=0) + timedelta(hours=1)
        end = start + timedelta(hours=hours[action])
        event = {'summary': title,
                 'start': {'dateTime': start.isoformat(), 'timeZone': TIMEZONE},
                 'end': {'dateTime': end.isoformat(), 'timeZone': TIMEZONE}}

    service.events().insert(calendarId=cal_id, body=event).execute()
    print("Added to calendar:", event['summary'])


if __name__ == '__main__':
    service = get_service()
    schedule_action(service, 'light')