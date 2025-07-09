from services.notify import send_pushover_notification
from typing import Dict

def record_user_details(email: str, name: str = 'not provided', notes: str = 'not provided') -> Dict[str, str]:
    send_pushover_notification(f"Recording {name}, with email {email}, and with notes {notes}")
    return {"Recorded": "Done"}

def get_record_user_details_json() -> Dict:
    record_user_details_json = {
        "name": "record_user_details",
        "description": "Use this tool to record that a user is interested in being in touch and provided an email address",
        "parameters": {
            "type": "object",
            "properties": {
                "email": {
                    "type": "string",
                    "description": "The email address of this user"
                },
                "name": {
                    "type": "string",
                    "description": "The user's name, if they provided it"
                },
                "notes": {
                    "type": "string",
                    "description": "Any additional information about the conversation that's worth recording to give context"
                }
            },
            "required": ["email"],
            "additionalProperties": False
        }
    }
    return record_user_details_json