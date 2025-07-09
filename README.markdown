# AI-Agent

A professional AI conversational agent designed to represent Abdullah Rizwan on a personal website, engaging potential employers or clients. The agent answers questions about Abdullah’s career, skills, and projects using a knowledge base, schedules meetings via Google Calendar, records user details and unknown questions, and sends real-time notifications via Pushover. Built with OpenAI’s `gpt-4o-mini`, Groq for response evaluation, Gradio for the UI, and integrated with Google Calendar API, this project showcases a robust, extensible system for professional interactions.

## Features
- **Conversational AI**: Powered by OpenAI’s `gpt-4o-mini`, the agent responds to user queries about Abdullah’s background, skills, and experience.
- **Knowledge Base**: Utilizes a summary, LinkedIn profile, and project descriptions to provide accurate, context-aware responses.
- **Tool Integration**:
  - **Schedule Meetings**: Creates events on Google Calendar with user-provided email and date.
  - **Record User Details**: Captures contact information (e.g., email, name) for potential leads.
  - **Record Unknown Questions**: Logs unanswerable questions for follow-up.
- **Pushover Notifications**: Sends real-time alerts for scheduled meetings, recorded details, and unknown questions.
- **Response Evaluation**: Uses Groq’s API to evaluate response quality, ensuring professional and accurate replies.
- **Gradio UI**: Provides an intuitive chat interface for user interactions.
- **Type-Safe Code**: Developed in Python with type hints, optimized for Cursor IDE’s Pyright.

## Prerequisites
- **Python**: Version 3.8 or higher.
- **Google Cloud Project**: With Google Calendar API enabled and OAuth 2.0 credentials set up.
- **API Keys**:
  - OpenAI API key for `gpt-4o-mini`.
  - Groq API key for response evaluation.
  - Pushover user key and API token for notifications.
- **Knowledge Base Files**:
  - `summary.txt`: A text summary of Abdullah’s background.
  - `linkedin_profile.pdf`: Abdullah’s LinkedIn profile in PDF format.
  - `project_description.pdf`: Details of Abdullah’s projects in PDF format.
- **System Requirements**: Internet connection for API calls, browser for Google OAuth authentication.

## Installation
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-username/ai-agent.git
   cd ai-agent
   ```

2. **Set Up a Virtual Environment** (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
   The `requirements.txt` includes:
   ```
   openai==1.30.0
   gradio==4.0.0
   pypdf==4.0.0
   python-dotenv==1.0.0
   requests==2.31.0
   pydantic==2.5.0
   google-auth-oauthlib==1.2.0
   google-auth-httplib2==0.2.0
   google-api-python-client==2.100.0
   ```

## Configuration
1. **Create `.env` File**:
   - In the project root, create a `.env` file with the following:
     ```
     OPENAI_API_KEY=your_openai_api_key
     GROQ_API_KEY=your_groq_api_key
     PUSHOVER_USER=your_pushover_user_key
     PUSHOVER_TOKEN=your_pushover_api_token
     ```
   - Obtain keys from:
     - OpenAI: [OpenAI Platform](https://platform.openai.com)
     - Groq: [Groq Console](https://console.groq.com)
     - Pushover: [Pushover Dashboard](https://pushover.net)

2. **Set Up Google Calendar API**:
   - Create a Google Cloud project and enable the Google Calendar API.
   - Configure the OAuth consent screen:
     - Set to **Internal** or **External** (add your email as a test user if Testing).
     - Add scope: `https://www.googleapis.com/auth/calendar.events`.
   - Create an OAuth 2.0 Client ID (Desktop App):
     - Download `credentials.json` and place it in the project root.
     - Add Authorized redirect URIs: `http://localhost:8080`, `urn:ietf:wg:oauth:2.0:oob`.
   - On first run, authenticate via browser to create `token.json`.

3. **Prepare Knowledge Base**:
   - Create a `data/knowledge_base` directory.
   - Place the following files:
     - `summary.txt`
     - `linkedin_profile.pdf`
     - `project_description.pdf`

## Usage
1. **Run the Application**:
   ```bash
   python main.py
   ```
   This launches the Gradio chat interface in your browser.

2. **Interact with the Agent**:
   - Ask questions about Abdullah’s career (e.g., “What projects has Abdullah worked on?”).
   - Schedule a meeting (e.g., “Schedule a meeting for July 15, 2025, at 10:00 AM with email daniel@example.com”).
   - Provide contact details (e.g., “My email is john@example.com, I’m interested in hiring”).
   - Ask unanswerable questions (e.g., “What’s the capital of Mars?”) to trigger logging.

3. **Monitor Notifications**:
   - Check Pushover for alerts about scheduled meetings, recorded details, or unknown questions.
   - Verify Google Calendar for meeting events.

## Project Structure
```
ai-agent/
├── data/
│   └── knowledge_base/
│       ├── summary.txt
│       ├── linkedin_profile.pdf
│       └── project_description.pdf
├── services/
│   ├── chat_interface.py
│   └── notify.py
├── tools/
│   ├── get_all_tools.py
│   ├── handle_tool_calls.py
│   ├── record_unknown_questions.py
│   ├── record_user_details.py
│   └── schedule_meeting.py
├── prompts/
│   └── get_all_prompts.py
├── agent/
│   ├── chat_llm.py
│   └── evaluator.py
├── main.py
├── .env
├── credentials.json
├── token.json
├── requirements.txt
└── README.md
```

- **services/**: Core functionality for chat and Pushover notifications.
- **tools/**: Tool definitions for scheduling, recording details, and logging questions.
- **prompts/**: System prompts for the agent and evaluator.
- **agent/**: LLM integration and response evaluation logic.
- **main.py**: Entry point launching the Gradio UI.

## Testing
1. **Test Prompts**:
   - **Career Questions**: “Tell me about Abdullah’s experience.”
   - **Meeting Scheduling**: “Schedule a meeting for July 15, 2025, at 10:00 AM with email daniel@example.com.”
   - **Contact Details**: “My email is john@example.com, I want to discuss a project.”
   - **Unknown Questions**: “What’s Abdullah’s favorite color?”

2. **Verify Outputs**:
   - **Google Calendar**: Check for meeting events.
   - **Pushover**: Confirm notifications for tools.
   - **Gradio UI**: Ensure responses are professional and accurate.

3. **Debugging**:
   - Check terminal logs for errors.
   - Delete `token.json` to re-authenticate Google Calendar if issues arise.

## Troubleshooting
- **Invalid Email Error**: Ensure prompts include valid emails (e.g., `user@domain.com`). The agent will request a valid email if missing.
- **Google Calendar Authentication**:
  - Verify `credentials.json` is in the project root.
  - Delete `token.json` and re-authenticate via browser.
  - Ensure `http://localhost:8080` is in Authorized redirect URIs in Google Cloud Console.
- **API Key Issues**:
  - Confirm `.env` contains valid keys for OpenAI, Groq, and Pushover.
- **Knowledge Base Errors**:
  - Ensure `data/knowledge_base` contains required files.
- **Gradio UI Issues**:
  - Run `pip install --upgrade gradio` if the interface fails to load.

## Contributing
Contributions are welcome! To contribute:
1. Fork the repository.
2. Create a feature branch (`git checkout -b feature/new-tool`).
3. Commit changes (`git commit -m "Add new tool"`).
4. Push to the branch (`git push origin feature/new-tool`).
5. Open a pull request.

Please ensure code follows Python type hints and passes Pyright checks in Cursor IDE.

## License
This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

## Contact
For questions or support, contact Abdullah Rizwan via [email@example.com](mailto:email@example.com) or through the website’s chat interface.