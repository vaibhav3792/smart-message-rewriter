
import re

class RewriteSafetyError(Exception):
    """Raised when a rewrite appears to change an action's status."""


# Ongoing verb form -> completed verb form.
ACTION_STATUS_PATTERNS = {
    "send": (r"\bsending\b", r"\bsent\b"),
    "submit": (r"\bsubmitting\b", r"\bsubmitted\b"),
    "publish": (r"\bpublishing\b", r"\bpublished\b"),
    "upload": (r"\buploading\b", r"\buploaded\b"),
    "review": (r"\breviewing\b", r"\breviewed\b"),
    "prepare": (r"\bpreparing\b", r"\bprepared\b"),
    "process": (r"\bprocessing\b", r"\bprocessed\b"),
    "investigate": (r"\binvestigating\b", r"\binvestigated\b"),
    "write": (r"\bwriting\b", r"\bwritten\b"),
    "build": (r"\bbuilding\b", r"\bbuilt\b"),
    "create": (r"\bcreating\b", r"\bcreated\b"),
    "complete": (r"\bcompleting\b", r"\bcompleted\b"),
    "finish": (r"\bfinishing\b", r"\bfinished\b"),
}


def detect_action_status_changes(original, rewritten):
    original = original.lower()
    rewritten = rewritten.lower()

    detected = []

    for action, (ongoing_pattern, completed_pattern) in ACTION_STATUS_PATTERNS.items():
        was_ongoing = re.search(ongoing_pattern, original)
        became_completed = re.search(completed_pattern, rewritten)

        if was_ongoing and became_completed:
            detected.append(action)

    return detected
