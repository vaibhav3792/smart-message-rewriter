from app.safety import RewriteSafetyError
from fastapi.testclient import TestClient

from app.main import app
from app.llm import LLMServiceError

client = TestClient(app)


def test_health_check():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_rewrite_success(monkeypatch):
    def fake_rewrite_message(message, tone, length, recipient):
        return "Could you please share the notes?"

    monkeypatch.setattr(
        "app.main.rewrite_message",
        fake_rewrite_message
    )

    response = client.post(
        "/api/rewrite",
        json={
            "message": "hey send me the notes",
            "tone": "friendly",
            "length": "concise",
            "recipient": "friend"
        }
    )

    assert response.status_code == 200
    assert response.json() == {
        "rewritten_message": "Could you please share the notes?"
    }


def test_rewrite_uses_default_preferences(monkeypatch):
    captured = {}

    def fake_rewrite_message(message, tone, length, recipient):
        captured["tone"] = tone
        captured["length"] = length
        captured["recipient"] = recipient
        return "Rewritten message"

    monkeypatch.setattr(
        "app.main.rewrite_message",
        fake_rewrite_message
    )

    response = client.post(
        "/api/rewrite",
        json={"message": "Hello, how are you?"}
    )

    assert response.status_code == 200
    assert captured == {
        "tone": "professional",
        "length": "balanced",
        "recipient": "colleague"
    }


def test_rewrite_rejects_invalid_tone():
    response = client.post(
        "/api/rewrite",
        json={
            "message": "Hello",
            "tone": "aggressive",
            "length": "balanced",
            "recipient": "colleague"
        }
    )

    assert response.status_code == 400
    assert "Invalid tone" in response.json()["detail"]


def test_rewrite_rejects_empty_message():
    response = client.post(
        "/api/rewrite",
        json={
            "message": "",
            "tone": "professional",
            "length": "balanced",
            "recipient": "colleague"
        }
    )

    assert response.status_code == 422


def test_rewrite_rejects_oversized_message():
    response = client.post(
        "/api/rewrite",
        json={
            "message": "a" * 5001
        }
    )

    assert response.status_code == 422




def test_rewrite_handles_service_error(monkeypatch):
    def fake_rewrite_message(message, tone, length, recipient):
        raise LLMServiceError("Groq service unavailable")

    monkeypatch.setattr(
        "app.main.rewrite_message",
        fake_rewrite_message
    )

    response = client.post(
        "/api/rewrite",
        json={"message": "Hello"}
    )

    assert response.status_code == 502
    assert response.json()["detail"] == (
        "The rewriting service is temporarily unavailable."
    )

def test_rewrite_handles_unexpected_runtime_error(monkeypatch):
    def fake_rewrite_message(message, tone, length, recipient):
        raise RuntimeError("Unexpected internal error")

    monkeypatch.setattr(
        "app.main.rewrite_message",
        fake_rewrite_message
    )

    error_client = TestClient(app, raise_server_exceptions=False)

    response = error_client.post(
        "/api/rewrite",
        json={"message": "Hello"}
    )

    assert response.status_code == 500

def test_rewrite_rejects_unsafe_action_status_change(monkeypatch):
    def fake_rewrite_message(message, tone, length, recipient):
        raise RewriteSafetyError(
            "Potential action-status change detected."
        )

    monkeypatch.setattr(
        "app.main.rewrite_message",
        fake_rewrite_message
    )

    response = client.post(
        "/api/rewrite",
        json={"message": "I am sending the report."}
    )

    assert response.status_code == 422
    assert response.json()["detail"] == (
        "Potential action-status change detected."
    )