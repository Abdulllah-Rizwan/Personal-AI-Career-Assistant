from pypdf import PdfReader
from pathlib import Path
from typing import List

class Prompt:
    def __init__(self, name: str, path_to_knowledge_base: Path):
        self.name = name
        self.path_to_knowledge_base = path_to_knowledge_base
        self.summary = ''
        self.linkedin_profile = ''
        self.project_description = ''
        self.parse_knowledge_base()

    def parse_knowledge_base(self) -> None:
        try:
            with open(self.path_to_knowledge_base / 'summary.txt', 'r') as f:
                self.summary = f.read()
        except FileNotFoundError:
            self.summary = "Summary not available."
        
        try:
            reader = PdfReader(self.path_to_knowledge_base / 'linkedin_profile.pdf')
            for page in reader.pages:
                text = page.extract_text()
                self.linkedin_profile += text or ""
        except FileNotFoundError:
            self.linkedin_profile = "LinkedIn profile not available."
        
        try:
            reader = PdfReader(self.path_to_knowledge_base / 'project_description.pdf')
            for page in reader.pages:
                text = page.extract_text()
                self.project_description += text or ""
        except FileNotFoundError:
            self.project_description = "Project description not available."

    def get_system_prompt(self) -> str:
        system_prompt = f"""You are acting as {self.name}. You are answering questions on {self.name}'s website, 
        particularly questions related to {self.name}'s career, background, skills, and experience. 
        Your responsibility is to represent {self.name} for interactions on the website as faithfully as possible. 
        You are given a summary of {self.name}'s background, LinkedIn profile, and project description to answer questions. 
        Be professional and engaging, as if talking to a potential client or future employer who came across the website. 
        If you don't know the answer, use the record_unknown_question tool to record the question.

        \n\n##Summary\n{self.summary}\n\n
        ##LinkedIn Profile\n{self.linkedin_profile}\n\n
        ##Project Description\n{self.project_description}\n\n

        With this context, please chat with the user, always staying in character as {self.name}."""
        return system_prompt
    
    def get_evaluator_system_prompt(self) -> str:
        evaluator_system_prompt = f"""You are an evaluator that decides whether a response to a question is acceptable. 
        You are provided with a conversation between a User and an Agent. Your task is to decide whether the Agent's latest response is acceptable quality. 
        The Agent is playing the role of {self.name} and is representing {self.name} on their website. 
        The Agent has been instructed to be professional and engaging, as if talking to a potential client or future employer who came across the website. 
        The Agent has been provided with context on {self.name} in the form of their summary, LinkedIn details, and project description. Here's the information:

        \n\n##Summary\n{self.summary}\n\n
        ##LinkedIn Profile\n{self.linkedin_profile}\n\n
        ##Project Description\n{self.project_description}\n\n

        With this context, evaluate the Agent's latest response to the User's question. 
        Return your evaluation as JSON with two fields: 'isAcceptable' (boolean) and 'feedback' (string), e.g., {{"isAcceptable": true, "feedback": "The response is accurate and professional."}}."""
        return evaluator_system_prompt
    
    def get_evaluator_user_prompt(self, reply: str, message: str, history: List[dict]) -> str:
        user_prompt = f"Here's the conversation between the User and the Agent:\n\n{history}\n\n"
        user_prompt += f"Here's the latest message from the User:\n\n{message}\n\n"
        user_prompt += f"Here's the latest response from the Agent:\n\n{reply}\n\n"
        user_prompt += "Please evaluate the response, replying with JSON containing 'isAcceptable' (boolean) and 'feedback' (string)."
        return user_prompt
    
    def system_prompt_to_rerun(self, reply: str, feedback: str, system_prompt: str) -> str:
        updated_system_prompt = system_prompt + "\n\n## Previous answer rejected\nYou just tried to reply, but the quality control rejected your reply\n"
        updated_system_prompt += f"## Your attempted answer:\n{reply}\n\n"
        updated_system_prompt += f"## Reason for rejection:\Evaluator\n{feedback}\n\n"
        return updated_system_prompt

def get_prompts() -> Prompt:
    return Prompt("Abdullah Rizwan", Path("data/knowledge_base"))