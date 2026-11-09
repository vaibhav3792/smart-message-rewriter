from app.config import (
    DEFAULT_TONE,
    DEFAULT_LENGTH,
    DEFAULT_RECIPIENT,
    validate_preferences,
)

from app.prompts import SYSTEM_PROMPT, build_user_prompt
from app.llm import generate_response

from app.safety import (
    detect_action_status_changes,
    RewriteSafetyError,
)


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

    # Check for potential action-status changes
    changed_actions = detect_action_status_changes(
        message,
        rewritten_message,
    )

    if changed_actions:
        raise RewriteSafetyError(
            "The rewrite may have changed the status of an action. "
            "Please try again or review the original message."
        )

    return rewritten_message