from tools.record_unknown_questions import get_record_unknown_questions_json
from tools.record_user_detail import get_record_user_details_json
from tools.schedule_meetings import get_schedule_meeting_json

def get_tools() -> list[dict]:
    tools = [
        {
            'type': 'function',
            'function': get_record_unknown_questions_json()
        },
        {
            'type': 'function',
            'function': get_record_user_details_json()
        },
        {
            'type': 'function',
            'function': get_schedule_meeting_json()
        }
    ]

    return tools
