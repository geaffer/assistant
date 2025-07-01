from google_calendar import get_all_events
from naver import fetch_recent_emails
from gpt_analysis import analyze_with_gpt
from push_notify import send_pushover
import os
from dotenv import load_dotenv

load_dotenv()

# 1. 일정 수집
print("📅 [1] 구글 캘린더 일정 수집 중...")
today_events, week_events, month_events = get_all_events()

# 2. 메일 수집
print("📩 [2] 네이버 메일 수집 중...")
NAVER_EMAIL = os.getenv("NAVER_EMAIL")
NAVER_APP_PASSWORD = os.getenv("NAVER_APP_PASSWORD")
emails = fetch_recent_emails(NAVER_EMAIL, NAVER_APP_PASSWORD)

# 3. GPT 분석
print("🧠 [3] GPT 요약 중...")

priority_emails = [mail for mail in emails if mail['priority']]
other_emails = [mail for mail in emails if not mail['priority']]

def format_email_block(title, email_list):
    if not email_list:
        return f"📭 {title}: 해당 없음"
    return f"✉️ {title}:\n" + "\n".join(
        [f"- {mail['subject']} (from {mail['from']})\n{mail['body'][:200].strip()}" for mail in email_list]
    )

combined_text = f"""
📆 [오늘 일정]
{today_events}

📅 [7일간 일정]
{week_events}

🗓️ [30일간 일정]
{month_events}

📧 [어제의 메일 요약]
{format_email_block('중요 메일', priority_emails)}

{format_email_block('기타 메일', other_emails)}
"""

summary = analyze_with_gpt(combined_text)

# 4. 알림 전송
print("📋 [4] 최종 요약 결과:")
print(summary)
send_pushover("📌 오늘 일정 및 메일 요약", summary)
