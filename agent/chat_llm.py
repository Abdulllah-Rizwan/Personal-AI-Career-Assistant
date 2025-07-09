from prompts.get_all_prompts import get_prompts
from dotenv import load_dotenv
from openai import OpenAI
from typing import List
import os

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

def get_model(model_name: str) -> OpenAI:
    if model_name == "OpenAI":
        return OpenAI(api_key=OPENAI_API_KEY)
    elif model_name == "Groq":
        return OpenAI(api_key=GROQ_API_KEY, base_url="https://api.groq.com/v1")
    else:
        raise ValueError(f"Unknown model: {model_name}")

def regenerate_response(reply: str, message: str, history: List[dict], feedback: str, system_prompt: str) -> str:
    prompts = get_prompts()
    system_prompt = prompts.system_prompt_to_rerun(reply, feedback, system_prompt)
    messages = [
        {"role": "system", "content": system_prompt}
    ] + history + [
        {"role": "user", "content": message}
    ]

    model = get_model("OpenAI")

    try:
        response = model.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages
        )
        return response.choices[0].message.content or ""
    except Exception as e:
        return f"Error regenerating response: {str(e)}"