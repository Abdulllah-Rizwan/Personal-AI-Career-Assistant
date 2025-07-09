import requests
import os

PUSHOVER_USER = os.getenv("PUSHOVER_USER")
PUSHOVER_TOKEN = os.getenv("PUSHOVER_TOKEN")

def send_pushover_notification(message: str) -> None:
    if not PUSHOVER_USER or not PUSHOVER_TOKEN:
        raise ValueError("Pushover credentials are missing")
    
    url = "https://api.pushover.net/1/messages.json"
    data = {
        "token": PUSHOVER_TOKEN,
        "user": PUSHOVER_USER,
        "message": message,
    }

    try:
        response = requests.post(url, data=data)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Pushover notification failed: {str(e)}")