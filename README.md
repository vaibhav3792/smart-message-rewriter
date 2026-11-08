# Smart Message Rewriter

A Python-based message rewriting assistant that improves clarity, grammar, and tone while preserving the original meaning and intent.

The application uses the Groq API to rewrite messages according to user-selected preferences.

## Features

- **Tone selection:** Professional, Friendly, Formal, Polite, Persuasive, and Casual.
- **Length control:** Concise, Balanced, and Detailed.
- **Recipient awareness:** Professor, Recruiter, Senior, Colleague, and Friend.
- **Input validation:** Rejects empty messages, invalid preferences, and messages exceeding the character limit.
- **Prompt-driven rewriting:** Preserves meaning and avoids inventing information.
- **Error handling:** Handles API connection failures, rate limits, and API errors.
- **Automated tests:** Tests core functionality using pytest and mocked API responses.

## Tech Stack

- Python
- Groq API
- Groq Python SDK
- python-dotenv
- pytest

## Project Structure

```text
smart-message-rewriter/
├── app/
│   ├── __init__.py
│   ├── config.py
│   ├── prompts.py
│   ├── llm.py
│   └── rewriter.py
├── tests/
│   ├── __init__.py
│   └── test_rewriter.py
├── .env
├── .gitignore
├── requirements.txt
└── README.md
```

## Setup

1. Clone the repository:

```bash
git clone https://github.com/vaibhav3792/smart-message-rewriter.git
cd smart-message-rewriter
```

2. Create and activate a virtual environment:

```bash
python -m venv .venv
```

Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key
```

## Usage

```python
from app.rewriter import rewrite_message

result = rewrite_message(
    message="hey sir i wanted to ask if there is any update regarding internship selection",
    tone="professional",
    length="concise",
    recipient="professor",
)

print(result)
```

The preference arguments are optional. If omitted, the application uses its default settings.

## Running Tests

Run the test suite from the project root:

```bash
pytest -q
```

## Current Development Status

The core rewriting logic, prompt construction, Groq API integration, input validation, and error handling are implemented.

The project will be extended with a user interface and deployment in subsequent development stages.