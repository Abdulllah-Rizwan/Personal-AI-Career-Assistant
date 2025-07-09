from tools.record_unknown_questions import record_unknown_questions
from openai.types.chat import ChatCompletionMessageToolCall
from tools.record_user_detail import record_user_details
from typing import List, Dict, Any
import json


TOOL_REGISTRY = {
    "record_unknown_questions": record_unknown_questions,
    "record_user_details": record_user_details,
   
}

def handle_tool_calls(tool_calls: List[ChatCompletionMessageToolCall]) -> List[Dict[str, Any]]:
    results: List[Dict[str, Any]] = []

    for tool_call in tool_calls:
        tool_name = tool_call.function.name
        try:
            arguments = json.loads(tool_call.function.arguments)
            tool = TOOL_REGISTRY.get(tool_name)
            if tool:
                result = tool(**arguments)
                results.append(
                    {'role': 'tool', 'content': json.dumps(result), 'tool_call_id': tool_call.id}
                )
            else:
                results.append(
                    {'role': 'tool', 'content': json.dumps({"error": f"Tool {tool_name} not found"}), 'tool_call_id': tool_call.id}
                )
        except json.JSONDecodeError:
            results.append(
                {'role': 'tool', 'content': json.dumps({"error": "Invalid tool arguments"}), 'tool_call_id': tool_call.id}
            )
    
    return results