
import re
from collections import Counter


def extract_numbers(text: str) -> list[str]:
    pattern = r"(?<![\w\d])\d[\d,]*(?:\.\d+)?%?"
    matches = re.findall(pattern, text)

    return [
        number.replace(",", "")
        for number in matches
    ]


def extract_dates(text: str) -> list[str]:
    """Extract common numeric and written date formats."""
    months = (
        r"January|February|March|April|May|June|July|August|"
        r"September|October|November|December"
    )

    patterns = [
        rf"\b\d{{1,2}}(?:st|nd|rd|th)?\s+(?:{months})\.?(?:\s*,?\s*\d{{4}})?",
        rf"\b(?:{months})\.?\s+\d{{1,2}}(?:st|nd|rd|th)?(?:,\s*\d{{4}})?",
        r"\b\d{1,2}[/-]\d{1,2}(?:[/-]\d{2,4})?\b",
    ]

    return [
        match.group(0).strip()
        for pattern in patterns
        for match in re.finditer(pattern, text, re.IGNORECASE)
    ]


def extract_times(text: str) -> list[str]:
    """Extract common 12-hour and 24-hour time formats."""
    patterns = [
        r"\b\d{1,2}(?::\d{2})?\s*(?:a\.?m\.?|p\.?m\.?)\b",
        r"\b(?:[01]?\d|2[0-3]):[0-5]\d\b",
    ]

    return [
        re.sub(r"[\s.]", "", match.group(0).lower())
        for pattern in patterns
        for match in re.finditer(pattern, text, re.IGNORECASE)
    ]


def extract_technical_identifiers(text: str) -> list[str]:
    """Extract common technical identifiers and IP addresses."""
    patterns = [
        r"\b[A-Z][A-Z0-9]*(?:_[A-Z0-9]+)+\b",
        r"\b(?:\d{1,3}\.){3}\d{1,3}\b",
        r"\bv?\d+\.\d+(?:\.\d+)?\b",
    ]

    return [
        match.group(0)
        for pattern in patterns
        for match in re.finditer(pattern, text)
    ]


def check_output_validity(output) -> dict:
    valid = isinstance(output, str) and bool(output.strip())

    return {
        "passed": valid,
        "details": None if valid else "Output is empty or invalid.",
    }


def check_number_preservation(original: str, output: str) -> dict:
    def normalize(numbers):
        return Counter(number.replace(",", "") for number in numbers)

    original_numbers = normalize(extract_numbers(original))
    output_numbers = normalize(extract_numbers(output))

    missing = list((original_numbers - output_numbers).elements())

    return {
        "passed": not missing,
        "missing": missing,
    }

def normalize_date(date: str) -> str:
    date = date.replace("\u202f", " ")
    date = date.replace("\xa0", " ")
    date = date.casefold().strip()
    date = re.sub(r"[.,]", "", date)
    date = " ".join(date.split())

    # Normalize "November 15" and "15 November"
    match = re.fullmatch(
        r"([a-z]+)\s+(\d{1,2})(?:st|nd|rd|th)?(?:\s+(\d{4}))?",
        date,
    )

    if match:
        month, day, year = match.groups()
        date = f"{day} {month}"
        if year:
            date += f" {year}"

    return date


def check_date_preservation(original: str, output: str) -> dict:
    original_dates = Counter(
        normalize_date(date) for date in extract_dates(original)
    )
    output_dates = Counter(
        normalize_date(date) for date in extract_dates(output)
    )

    missing = list((original_dates - output_dates).elements())

    return {
        "passed": not missing,
        "missing": missing,
    }

def check_time_preservation(original: str, output: str) -> dict:
    original_times = Counter(extract_times(original))
    output_times = Counter(extract_times(output))

    missing = list((original_times - output_times).elements())

    return {
        "passed": not missing,
        "missing": missing,
    }


def check_technical_identifiers(original: str, output: str) -> dict:
    original_ids = Counter(extract_technical_identifiers(original))
    output_ids = Counter(extract_technical_identifiers(output))

    missing = list((original_ids - output_ids).elements())

    return {
        "passed": not missing,
        "missing": missing,
    }


def check_length_adherence(
    original: str,
    output: str,
    requested_length: str,
) -> dict:
    original_words = len(original.split())
    output_words = len(output.split())

    ratio = output_words / max(original_words, 1)

    # These are broad heuristics, not semantic quality judgments.
    ranges = {
        "concise": (0, 1.35),
        "balanced": (0.60, 1.80),
        "detailed": (0.80, float("inf")),
    }


    minimum, maximum = ranges[requested_length]
    passed = minimum <= ratio <= maximum

    return {
        "passed": passed,
        "original_word_count": original_words,
        "output_word_count": output_words,
        "ratio": round(ratio, 2),
        "details": None if passed else "Output length may not match the requested preference.",
    }
