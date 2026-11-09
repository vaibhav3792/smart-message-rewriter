# Smart Message Rewriter - Frontend

React, Vite, and TypeScript frontend for the Smart Message Rewriter.

The frontend communicates with a FastAPI backend that uses Groq to rewrite messages.

## Requirements

- Node.js and npm
- The Smart Message Rewriter backend running locally

## Setup

From the `frontend` directory, run:

```powershell
npm install
Copy-Item .env.example .env
```

The `.env` file configures the backend URL:

```env
VITE_API_BASE_URL=http://localhost:8000
```

## Run locally

First, start the backend from the project root in a separate terminal:

```powershell
.\.venv\Scripts\Activate.ps1
uvicorn app.main:app --reload
```

Then start the frontend:

```powershell
cd frontend
npm run dev
```

Open the local URL printed by Vite (usually http://localhost:5173).

## Production build

To verify the frontend build:

```powershell
npm run build
```

## Project structure

- `src/App.tsx` - Main application UI and interaction state
- `src/api/rewriter.ts` - API communication with the FastAPI backend
- `src/styles.css` - Application styling
- `src/main.tsx` - Frontend entry point
