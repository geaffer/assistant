import requests
import os
from dotenv import load_dotenv

load_dotenv()

def send_pushover(title, message):
    token = os.getenv("PUSHOVER_APP_TOKEN")
    user = os.getenv("PUSHOVER_USER_KEY")

    response = requests.post(
        "https://api.pushover.net/1/messages.json",
        data={
            "token": token,
            "user": user,
            "title": title,
            "message": message,
        }
    )
    print(f"🔔 Pushover 전송: {response.status_code} | {response.text}")
