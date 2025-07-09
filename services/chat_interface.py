from agent.chat_llm import get_model, regenerate_response
from tools.handle_tool_calls import handle_tool_calls
from prompts.get_all_prompts import get_prompts
from tools.get_all_tools import get_tools
from agent.evaluator import Evaluator
from typing import List, Union

def chat(message: str, history: List[dict]) -> str:
    prompts = get_prompts()
    system_prompt = prompts.get_system_prompt()
    messages = [
        {"role": "system", "content": system_prompt}
    ] + history + [
        {"role": "user", "content": message}
    ]

    chat_model = get_model('OpenAI')
    tools = get_tools()

    while True:

        try:
            response = chat_model.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages,
                tools=tools,
                tool_choice="auto"
            )
        except Exception as e:
            return f"Error generating response: {str(e)}"

        finish_reason = response.choices[0].finish_reason

        if finish_reason == "tool_calls":
            assistant_message = response.choices[0].message
            tool_calls = assistant_message.tool_calls
            tool_results = handle_tool_calls(tool_calls)
            # Append the assistant message as a dict
            messages.append({
                "role": "assistant",
                "content": assistant_message.content,  # Should be None or a string
                "tool_calls": [tc.to_dict() for tc in tool_calls],
            })
            # Append tool results (already dicts)
            messages.extend(tool_results)
        else:
            break
          
    reply = response.choices[0].message.content or ""
    evaluator = Evaluator()
    evaluator_response = evaluator.evaluate(reply, message, history)
    if evaluator_response.isAcceptable:
        return reply
    else:
        return regenerate_response(reply, message, history, evaluator_response.feedback, system_prompt)