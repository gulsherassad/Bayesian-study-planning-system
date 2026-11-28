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


def clear_day(service, cal_id, day):
    # remove anything already planned for that day so it doesn't double book
    start = datetime(day.year, day.month, day.day, tzinfo=tz)
    events = service.events().list(calendarId=cal_id, timeMin=start.isoformat(),
                                   timeMax=(start + timedelta(days=1)).isoformat()).execute()
    for event in events.get('items', []):
        service.events().delete(calendarId=cal_id, eventId=event['id']).execute()


def schedule_action(service, action, day=None, focus=None):
    today = datetime.now(tz).date()
    if day is None:
        day = today

    cal_id = get_planner_calendar(service)
    clear_day(service, cal_id, day)

    if action == 'rest':
        event = {'summary': 'Rest day',
                 'start': {'date': day.isoformat()},
                 'end': {'date': (day + timedelta(days=1)).isoformat()}}
    else:
        hours = {'intense': 5, 'practice': 2, 'light': 1}
        names = {'intense': 'Intense study block', 'practice': 'Practice problems', 'light': 'Light review'}
        title = names[action]
        if focus:
            title = title + ': focus on ' + focus

        # today starts at the next full hour, other days start at 10am
        if day == today:
            start = datetime.now(tz).replace(minute=0, second=0, microsecond=0) + timedelta(hours=1)
        else:
            start = datetime(day.year, day.month, day.day, 10, tzinfo=tz)
        end = start + timedelta(hours=hours[action])
        event = {'summary': title,
                 'start': {'dateTime': start.isoformat(), 'timeZone': TIMEZONE},
                 'end': {'dateTime': end.isoformat(), 'timeZone': TIMEZONE}}

    service.events().insert(calendarId=cal_id, body=event).execute()
    print("  added to calendar:", day, event['summary'])


if __name__ == '__main__':
    service = get_service()
    schedule_action(service, 'light')