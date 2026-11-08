from app.config import (
    DEFAULT_TONE,
    DEFAULT_LENGTH,
    DEFAULT_RECIPIENT,
    validate_preferences,
)

from app.prompts import SYSTEM_PROMPT, build_user_prompt
from app.llm import generate_response

MAX_MESSAGE_LENGTH = 5000

def rewrite_message(
    message,
    tone=DEFAULT_TONE,
    length=DEFAULT_LENGTH,
    recipient=DEFAULT_RECIPIENT,
):
    # Validate message
    if not isinstance(message, str) or not message.strip():
        raise ValueError("Message cannot be empty.")

    message = message.strip()

    if len(message) > MAX_MESSAGE_LENGTH:
        raise ValueError(
        f"Message exceeds the maximum length of {MAX_MESSAGE_LENGTH} characters."
        )

    # Validate and normalize preferences
    tone, length, recipient = validate_preferences(
        tone, length, recipient
    )

    # Construct the user prompt
    user_prompt = build_user_prompt(
        message, tone, length, recipient
    )

    # Generate rewritten message
    rewritten_message = generate_response(
        SYSTEM_PROMPT, user_prompt
    )

    return rewritten_message