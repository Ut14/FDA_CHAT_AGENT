
# FDA Chat Agent

A simple, FastAPI-based agentic system that uses FDA drug data to answer user questions via a web chat interface. Powered by local tools, asynchronous Python, and no vector databases.




## Features

- Ask questions like:
    - "What are the adverse effects of aspirin?"
    - "Show drugs in the nonsteroidal pharmacologic class."
    - "How many patients reported reactions to nonsteroidal drugs?"
    - "List adverse events between January and December 2023."
- Lightweight frontend in plain HTML/JS.

- Backend: FastAPI + async tool-calling agent logic.

- SQL or structured data querying (via db.py).

- No external LLM needed — tool routing is rule-based (can be extended with Qwen/LLMs).




## Installation

1. Clone the repository:

```bash
git clone https://github.com/Ut14/FDA_CHAT_AGENT.git
cd FDA_CHAT_AGENT
```
2. Install dependencies:

```bash
pip install -r requirements.txt
```
3. Start the FastAPI server

4. Open the Chat Interface
Go to your browser:

👉 http://127.0.0.1:8000

You’ll see a simple chat UI where you can ask questions.
## License

This project is licensed under the MIT License.

