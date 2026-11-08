import pytest

from app.config import validate_preferences


def test_valid_preferences():
    result = validate_preferences(
        "Professional",
        "Concise",
        "Professor"
    )

    assert result == ("professional", "concise", "professor")


def test_preferences_are_normalized():
    result = validate_preferences(
        " PROFESSIONAL ",
        "Concise ",
        " PROFESSOR"
    )

    assert result == ("professional", "concise", "professor")


def test_invalid_tone():
    with pytest.raises(ValueError, match="Invalid tone"):
        validate_preferences("angry", "concise", "professor")


def test_invalid_length():
    with pytest.raises(ValueError, match="Invalid length"):
        validate_preferences("professional", "short", "professor")


def test_invalid_recipient():
    with pytest.raises(ValueError, match="Invalid recipient"):
        validate_preferences("professional", "concise", "manager")

########################################################################

from app.rewriter import rewrite_message


def test_rewrite_message_success(monkeypatch):
    def fake_generate_response(system_prompt, user_prompt):
        return "Could you please share the notes?"

    monkeypatch.setattr(
        "app.rewriter.generate_response",
        fake_generate_response
    )

    result = rewrite_message(
        "hey send me the notes",
        tone="friendly",
        length="concise",
        recipient="friend"
    )

    assert result == "Could you please share the notes?"


def test_rewrite_message_uses_defaults(monkeypatch):
    captured_prompts = {}

    def fake_generate_response(system_prompt, user_prompt):
        captured_prompts["system"] = system_prompt
        captured_prompts["user"] = user_prompt
        return "Rewritten message"

    monkeypatch.setattr(
        "app.rewriter.generate_response",
        fake_generate_response
    )

    result = rewrite_message("hey how are you")

    assert result == "Rewritten message"
    assert "professional" in captured_prompts["user"]
    assert "balanced" in captured_prompts["user"]
    assert "colleague" in captured_prompts["user"]


@pytest.mark.parametrize("message", ["", "   ", None, 123])
def test_rejects_invalid_message(message):
    with pytest.raises(ValueError, match="Message cannot be empty"):
        rewrite_message(message)



from app.rewriter import MAX_MESSAGE_LENGTH


def test_rejects_message_exceeding_max_length():
    message = "a" * (MAX_MESSAGE_LENGTH + 1)

    with pytest.raises(ValueError, match="maximum length"):
        rewrite_message(message)


def test_accepts_message_at_max_length(monkeypatch):
    monkeypatch.setattr(
        "app.rewriter.generate_response",
        lambda system_prompt, user_prompt: "Rewritten message"
    )

    message = "a" * MAX_MESSAGE_LENGTH

    result = rewrite_message(message)

    assert result == "Rewritten message"


#################################################################################

from app.prompts import build_user_prompt


def test_user_prompt_contains_preferences():
    prompt = build_user_prompt(
        "hey sir any update?",
        "professional",
        "concise",
        "professor"
    )

    assert "professional" in prompt
    assert "concise" in prompt
    assert "professor" in prompt
    assert "hey sir any update?" in prompt


################################################################


from groq import APIConnectionError, RateLimitError
import httpx    
from app.llm import generate_response



def test_llm_handles_rate_limit_error(monkeypatch):
    request = httpx.Request(
        "POST",
        "https://api.groq.com/openai/v1/chat/completions"
    )

    response = httpx.Response(
        status_code=429,
        request=request
    )

    def fake_api_call(**kwargs):
        raise RateLimitError(
            "Rate limit exceeded",
            response=response,
            body=None
        )

    monkeypatch.setattr(
        "app.llm.client.chat.completions.create",
        fake_api_call
    )

    with pytest.raises(RuntimeError, match="rate limit"):
        generate_response("system prompt", "user prompt")
