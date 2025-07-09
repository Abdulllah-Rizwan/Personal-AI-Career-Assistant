from google_auth_oauthlib.flow import InstalledAppFlow
from services.notify import send_pushover_notification
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from typing import Dict
import datetime
import os
import re

def schedule_meeting(email: str, preferred_date: str, notes: str = "not provided") -> Dict[str, str]:
    
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    if not re.match(email_regex, email):
        error_msg = f"Invalid email address: {email}. Must be a valid email (e.g., user@domain.com)."
        send_pushover_notification(error_msg)
        return {"Scheduled": "Failed", "error": error_msg}

    SCOPES = ['https://www.googleapis.com/auth/calendar.events']
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        try:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=8080)
            with open('token.json', 'w') as token:
                token.write(creds.to_json())
        except Exception as e:
            error_msg = f"Authentication failed: {str(e)}. Requested redirect_uri: http://localhost:8080"
            send_pushover_notification(error_msg)
            return {"Scheduled": "Failed", "error": error_msg}

    try:
        service = build('calendar', 'v3', credentials=creds)
        start_time = datetime.datetime.strptime(preferred_date, "%Y-%m-%d %I:%M %p")
        end_time = start_time + datetime.timedelta(hours=1)
        event = {
            'summary': f'Meeting with {email}',
            'description': notes,
            'start': {
                'dateTime': start_time.isoformat(),
                'timeZone': 'UTC',
            },
            'end': {
                'dateTime': end_time.isoformat(),
                'timeZone': 'UTC',
            },
            'attendees': [{'email': email}],
            'reminders': {
                'useDefault': True
            }
        }
        event = service.events().insert(calendarId='primary', body=event).execute()
        send_pushover_notification(f"Scheduled meeting with {email} on {preferred_date}. Notes: {notes}")
        return {"Scheduled": "Done", "event_id": event.get('id')}
    except ValueError as e:
        error_msg = f"Invalid date format for {email}: {str(e)}. Use YYYY-MM-DD HH:MM AM/PM."
        send_pushover_notification(error_msg)
        return {"Scheduled": "Failed", "error": error_msg}
    except Exception as e:
        error_msg = f"Failed to schedule meeting with {email}: {str(e)}"
        send_pushover_notification(error_msg)
        return {"Scheduled": "Failed", "error": error_msg}

def get_schedule_meeting_json() -> Dict:
    return {
        "name": "schedule_meeting",
        "description": "Use this tool to schedule a meeting on Google Calendar when a user requests a call or meeting. Ensure the email is a valid email address (e.g., user@domain.com).",
        "parameters": {
            "type": "object",
            "properties": {
                "email": {
                    "type": "string",
                    "description": "The user's valid email address for the meeting invitation (e.g., user@domain.com)"
                },
                "preferred_date": {
                    "type": "string",
                    "description": "Preferred date and time for the meeting in 'YYYY-MM-DD HH:MM AM/PM' format (e.g., '2025-07-15 10:00 AM')"
                },
                "notes": {
                    "type": "string",
                    "description": "Additional notes about the meeting"
                }
            },
            "required": ["email", "preferred_date"],
            "additionalProperties": False
        }
    }