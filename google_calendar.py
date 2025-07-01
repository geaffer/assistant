import os
import json
import datetime
import pytz
from googleapiclient.discovery import build
from google.oauth2 import service_account

SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

def get_service():
    # Railway 환경 변수에서 서비스 계정 JSON 로드
    service_account_info = json.loads(os.getenv("GOOGLE_SERVICE_ACCOUNT_JSON"))
    credentials = service_account.Credentials.from_service_account_info(
        service_account_info,
        scopes=SCOPES
    )
    return build('calendar', 'v3', credentials=credentials)

def get_events_range(start, end, service):
    events_result = service.events().list(
        calendarId='sela11367@gmail.com',
        timeMin=start.isoformat(),
        timeMax=end.isoformat(),
        singleEvents=True,
        orderBy='startTime'
    ).execute()
    return events_result.get('items', [])

def format_events(events, title):
    if not events:
        return f"{title}: 없음"
    output = f"{title}:\n"
    for event in events:
        start_raw = event['start'].get('dateTime', event['start'].get('date'))
        summary = event.get('summary', '제목 없음')
        try:
            dt = datetime.datetime.fromisoformat(start_raw).astimezone(pytz.timezone('Asia/Seoul'))
            time_str = dt.strftime("%Y-%m-%d %H:%M")
        except:
            time_str = start_raw
        output += f"- {time_str} | {summary}\n"
    return output

def get_all_events():
    tz = pytz.timezone('Asia/Seoul')
    now = datetime.datetime.now(tz)
    service = get_service()

    today_start = now.replace(hour=0, minute=0, second=0)
    today_end = today_start + datetime.timedelta(days=1)
    week_end = today_start + datetime.timedelta(days=7)
    month_end = today_start + datetime.timedelta(days=30)

    today_events = get_events_range(today_start, today_end, service)
    week_events = get_events_range(today_start, week_end, service)
    month_events = get_events_range(today_start, month_end, service)

    return (
        format_events(today_events, "오늘 일정"),
        format_events(week_events, "7일간 일정"),
        format_events(month_events, "30일간 일정")
    )
