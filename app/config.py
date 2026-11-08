
# Supported rewriting preferences

VALID_TONES = [
    "professional",
    "friendly",
    "formal",
    "polite",
    "persuasive",
    "casual",
]

VALID_LENGTHS = [
    "concise",
    "balanced",
    "detailed",
]

VALID_RECIPIENTS = [
    "professor",
    "recruiter",
    "senior",
    "colleague",
    "friend",
]

# Default preferences

DEFAULT_TONE = "professional"
DEFAULT_LENGTH = "balanced"
DEFAULT_RECIPIENT = "colleague"


def validate_preferences(tone, length, recipient):
    # Normalize inputs
    tone = tone.strip().lower()
    length = length.strip().lower()
    recipient = recipient.strip().lower()

    # Validate preferences
    if tone not in VALID_TONES:
        raise ValueError(f"Invalid tone: {tone}. Choose from {VALID_TONES}")

    if length not in VALID_LENGTHS:
        raise ValueError(f"Invalid length: {length}. Choose from {VALID_LENGTHS}")

    if recipient not in VALID_RECIPIENTS:
        raise ValueError(
            f"Invalid recipient: {recipient}. Choose from {VALID_RECIPIENTS}"
        )

    return tone, length, recipient
