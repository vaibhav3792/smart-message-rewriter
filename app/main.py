from app.safety import RewriteSafetyError
from fastapi import FastAPI, HTTPException
from app.schemas import RewriteRequest, RewriteResponse
from app.rewriter import rewrite_message
from fastapi.middleware.cors import CORSMiddleware
from app.llm import LLMServiceError
import os

app = FastAPI(
    title="Smart Message Rewriter API",
    description="An API for rewriting messages using AI.",
    version="1.0.0",
)


allowed_origins = [
    origin.strip()
    for origin in os.getenv(
        "FRONTEND_ORIGINS",
        "http://localhost:5173,http://127.0.0.1:5173",
    ).split(",")
    if origin.strip()
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"],
)


@app.get("/")
def root():
    return {
        "message": "Smart Message Rewriter API is running."
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }


@app.post("/api/rewrite", response_model=RewriteResponse)
def rewrite(request: RewriteRequest):
    try:
        rewritten = rewrite_message(
            message=request.message,
            tone=request.tone,
            length=request.length,
            recipient=request.recipient,
        )

        return RewriteResponse(
            rewritten_message=rewritten
        )
    except RewriteSafetyError as e:
        raise HTTPException(
            status_code=422,
            detail=str(e),
        ) from e
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        ) from e

    except LLMServiceError as e:
        raise HTTPException(
            status_code=502,
            detail="The rewriting service is temporarily unavailable.",
        ) from e
