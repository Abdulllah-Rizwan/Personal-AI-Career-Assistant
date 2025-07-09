from services.notify import send_pushover_notification
from typing import Dict

def record_unknown_questions(question: str) -> Dict[str, str]:
    send_pushover_notification(f"Unknown question: {question}")
    return {"Recorded": "Done"}

def get_record_unknown_questions_json() -> Dict:
    record_unknown_question_json = {
        "name": "record_unknown_questions",
        "description": "Always use this tool to record any question that couldn't be answered as you didn't know the answer. If you don't know the answer, record the question and say you don't know the answer but you will find out and get back to them.",
        "parameters": {
            "type": "object",
            "properties": {
                "question": {
                    "type": "string",
                    "description": "The question that couldn't be answered"
                },
            },
            "required": ["question"],
            "additionalProperties": False
        }
    }
    return record_unknown_question_json