from openai.types.chat import ChatCompletionMessageParam
from prompts.get_all_prompts import get_prompts
from agent.chat_llm import get_model
from pydantic import BaseModel
from typing import List


class Evaluation_Schema(BaseModel):
    isAcceptable: bool
    feedback: str


class Evaluator:
    def __init__(self):
        self.model = get_model('Groq')
        self.prompt = get_prompts()
    
    def evaluate(self, reply: str, message: str, history: List[dict]) -> Evaluation_Schema:
        messages: List[ChatCompletionMessageParam] = [
            {
                "role": "system",
                "content": self.prompt.get_evaluator_system_prompt()
            },
            {
                "role": "user",
                "content": self.prompt.get_evaluator_user_prompt(reply, message, history)
            }
        ]

        try:
            response = self.model.chat.completions.create(
                model='grok-3-mini',  
                messages=messages
            )

            response_content = response.choices[0].message.content
            if response_content is None:
                raise ValueError("Received empty response from the model")
            
            try:
                return Evaluation_Schema.model_validate_json(response_content)
            except ValueError:
                return Evaluation_Schema(isAcceptable=False, feedback=f"Invalid response format: {response_content}")
        except Exception as e:
            return Evaluation_Schema(isAcceptable=False, feedback=f"Evaluation error: {str(e)}")