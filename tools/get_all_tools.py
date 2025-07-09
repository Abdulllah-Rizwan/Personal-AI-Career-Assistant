from tools.record_unknown_questions import get_record_unknown_questions_json
from tools.record_user_detail import get_record_user_details_json

def get_tools() -> list[dict]:
    tools = [
        {
            'type': 'function',
            'function': get_record_unknown_questions_json()
        },
        {
            'type': 'function',
            'function': get_record_user_details_json()
        }
    ]

    return tools