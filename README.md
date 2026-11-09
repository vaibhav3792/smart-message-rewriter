# Smart Message Rewriter

A full-stack AI application that rewrites messages according to the desired tone, length, and recipient while preserving the original meaning and important details.

**Live Application:** https://smart-message-rewriter.vercel.app/

**Backend API:** https://smart-message-rewriter-api.onrender.com/

**API Documentation:** https://smart-message-rewriter-api.onrender.com/docs

## Overview

Smart Message Rewriter helps users communicate more effectively by transforming rough or informal messages into clearer, more appropriate versions.

Users can provide a message, select a tone and preferred length, optionally specify the recipient, and receive an AI-generated rewrite.

The application uses a React frontend, a FastAPI backend, and the Groq API for language model inference.

## Features

- **Tone control:** Rewrite messages in different tones.
- **Length control:** Choose the desired response length.
- **Recipient context:** Provide recipient information to guide the rewrite.
- **Meaning preservation:** Designed to retain important facts, figures, dates, and instructions from the original message.
- **Input validation:** Validate requests before processing.
- **Safety checks:** Apply safeguards to detect problematic rewriting outputs.
- **Error handling:** Handle validation errors and failures from the LLM service.
- **Responsive interface:** Use the application through a web-based frontend.

## Tech Stack

| Layer | Technologies |
|---|---|
| Frontend | React, TypeScript, Vite |
| Backend | Python, FastAPI |
| Validation | Pydantic |
| LLM Integration | Groq API |
| Model | `openai/gpt-oss-120b` |
| Testing | Pytest, FastAPI TestClient |
| Frontend Hosting | Vercel |
| Backend Hosting | Render |

## Architecture

```text
                  User
                   |
                   v
          React + TypeScript
             (Vercel)
                   |
                   | HTTP Request
                   v
             FastAPI API
               (Render)
                   |
                   v
          Request Validation
              (Pydantic)
                   |
                   v
           Rewriting Pipeline
                   |
          +--------+--------+
          |                 |
          v                 v
      Prompt Logic      Safety Checks
          |
          v
       Groq API
          |
          v
     LLM Response
          |
          v
     Output Validation
          |
          v
       API Response
          |
          v
      React Frontend
```

## Project Structure

```text
smart-message-rewriter/
│
├── app/
│   ├── __init__.py
│   ├── config.py
│   ├── prompts.py
│   ├── llm.py
│   ├── rewriter.py
│   ├── safety.py
│   ├── schemas.py
│   └── main.py
│
├── frontend/
│   ├── src/
│   │   ├── api/
│   │   │   └── rewriter.ts
│   │   ├── App.tsx
│   │   ├── main.tsx
│   │   └── styles.css
│   ├── .env.example
│   ├── package.json
│   └── vite.config.ts
│
├── tests/
│   ├── __init__.py
│   ├── test_api.py
│   └── test_rewriter.py
│
├── .gitignore
├── render.yaml
├── requirements.txt
└── README.md
```

## Getting Started

### Prerequisites

- Python 3.12+
- Node.js and npm
- A Groq API key

### 1. Clone the repository

```bash
git clone https://github.com/vaibhav3792/smart-message-rewriter.git

cd smart-message-rewriter
```

### 2. Backend Setup

Create and activate a virtual environment.

**Windows PowerShell:**

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
pip install -r requirements.txt
```

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key
FRONTEND_ORIGINS=http://localhost:5173,http://127.0.0.1:5173
```

Start the backend:

```powershell
uvicorn app.main:app --reload
```

The backend will be available at:

```text
http://localhost:8000
```

Interactive API documentation:

```text
http://localhost:8000/docs
```

### 3. Frontend Setup

Open another terminal:

```powershell
cd frontend
npm install
```

Create a `.env` file inside the `frontend` directory:

```env
VITE_API_BASE_URL=http://localhost:8000
```

Start the development server:

```powershell
npm run dev
```

The frontend will be available at:

```text
http://localhost:5173
```

## API Reference

### `GET /`

Returns a message indicating that the API is running.

### `GET /health`

Health-check endpoint.

Example response:

```json
{
  "status": "healthy"
}
```

### `POST /api/rewrite`

Accepts a message and rewriting preferences, then returns the rewritten message.

Example request:

```json
{
  "message": "hey, can you send me the project update by tomorrow?",
  "tone": "professional",
  "length": "medium",
  "recipient": "Project Manager"
}
```

Example response:

```json
{
  "rewritten_message": "Could you please share the project update by tomorrow?"
}
```

The exact response depends on the input and model output.

## Running Tests

Run the backend test suite from the project root:

```powershell
python -m pytest -q
```

The test suite covers API behavior and rewriting logic.

Build the frontend for production:

```powershell
cd frontend
npm run build
```

## Deployment

The application is deployed using:

- **Frontend:** Vercel
- **Backend:** Render

### Backend Deployment

The repository includes `render.yaml` for configuring the backend service.

Configure the following environment variables in Render:

| Variable | Description |
|---|---|
| `GROQ_API_KEY` | API key used for Groq inference |
| `FRONTEND_ORIGINS` | Comma-separated list of permitted frontend origins |

The deployment configuration uses:

```text
Build Command:
pip install -r requirements.txt

Start Command:
uvicorn app.main:app --host 0.0.0.0 --port $PORT

Health Check Path:
/health
```

### Frontend Deployment

Deploy the `frontend` directory through Vercel.

Configure the environment variable:

```env
VITE_API_BASE_URL=https://smart-message-rewriter-api.onrender.com
```

This connects the deployed frontend to the production backend.

## Current Limitations

- The backend runs on Render's free tier, so the first request after inactivity may take longer while the service wakes up.
- Model availability and response times depend on the Groq API and its rate limits.
- The application currently does not include user authentication or persistent message history.

## Future Improvements

- Add user authentication and message history.
- Introduce more customization options for rewriting.
- Expand automated evaluation of meaning preservation and output quality.
- Improve monitoring and observability.
- Add support for additional language models.