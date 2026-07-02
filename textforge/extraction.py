"""Text pattern extraction — emails, URLs, phones, IPs, UUIDs, dates, colors."""

from __future__ import annotations

import re
from dataclasses import dataclass


@dataclass(frozen=True)
class Extraction:
    """A single extracted pattern match."""

    value: str
    start: int
    end: int
    pattern: str

    def __repr__(self) -> str:
        return f"Extraction({self.pattern!r}, {self.value!r}, pos={self.start}-{self.end})"


# Compiled patterns
_EMAIL_RE = re.compile(r"[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}")

_URL_RE = re.compile(
    r"https?://[^\s<>\[\](){}\"']+"
    r"|www\.[^\s<>\[\](){}\"']+\.[a-zA-Z]{2,}"
)

_PHONE_RE = re.compile(
    r"(?:\+?\d{1,3}[\s\-]?)?"  # country code
    r"(?:\(?\d{2,4}\)?[\s\-]?)"  # area code
    r"\d{3,4}[\s\-]?\d{3,4}"  # main number
)

_IP_V4_RE = re.compile(
    r"\b(?:(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)\.){3}"
    r"(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)\b"
)

_IP_V6_RE = re.compile(
    r"\b(?:[0-9a-fA-F]{1,4}:){7}[0-9a-fA-F]{1,4}\b"
    r"|(?:[0-9a-fA-F]{1,4}:){1,7}:"
    r"|::(?:[0-9a-fA-F]{1,4}:){0,5}[0-9a-fA-F]{1,4}\b"
)

_UUID_RE = re.compile(
    r"\b[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}"
    r"-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}\b"
)

_DATE_RE = re.compile(
    r"\b(?:\d{4}[\-/\.]\d{1,2}[\-/\.]\d{1,2})"  # YYYY-MM-DD
    r"|\b(?:\d{1,2}[\-/\.]\d{1,2}[\-/\.]\d{4})"  # DD-MM-YYYY
    r"|\b(?:\d{1,2}[\s]+(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*[\s,]+\d{4})"  # DD Month YYYY
    r"|\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*[\s]+\d{1,2}[\s,]+\d{4}",  # Month DD, YYYY
    re.IGNORECASE,
)

_HEX_COLOR_RE = re.compile(r"(?<![0-9a-fA-F])(?:#|0x)[0-9a-fA-F]{3}(?:[0-9a-fA-F]{3})?(?![0-9a-fA-F])")


def extract_emails(text: str) -> list[Extraction]:
    """Extract all email addresses from text.

    Args:
        text: Input text.

    Returns:
        List of Extraction objects with email values and positions.
    """
    return [
        Extraction(value=m.group(), start=m.start(), end=m.end(), pattern="email") for m in _EMAIL_RE.finditer(text)
    ]


def extract_urls(text: str) -> list[Extraction]:
    """Extract all URLs from text.

    Handles http://, https://, and bare www. URLs.

    Args:
        text: Input text.

    Returns:
        List of Extraction objects with URL values and positions.
    """
    return [Extraction(value=m.group(), start=m.start(), end=m.end(), pattern="url") for m in _URL_RE.finditer(text)]


def extract_phone_numbers(text: str) -> list[Extraction]:
    """Extract phone numbers from text.

    Handles international formats, with or without country code,
    various separators (spaces, dashes, dots, parentheses).

    Args:
        text: Input text.

    Returns:
        List of Extraction objects with phone number values and positions.
    """
    results = []
    for m in _PHONE_RE.finditer(text):
        digits_only = re.sub(r"\D", "", m.group())
        # Filter out matches that are too short to be real phone numbers
        if 7 <= len(digits_only) <= 15:
            results.append(Extraction(value=m.group().strip(), start=m.start(), end=m.end(), pattern="phone"))
    return results


def extract_ip_addresses(text: str) -> list[Extraction]:
    """Extract IPv4 and IPv6 addresses from text.

    Validates IPv4 octets are in range 0-255.

    Args:
        text: Input text.

    Returns:
        List of Extraction objects with IP address values and positions.
    """
    results = []
    for m in _IP_V4_RE.finditer(text):
        # Validate each octet is 0-255
        octets = m.group().split(".")
        if all(0 <= int(o) <= 255 for o in octets):
            results.append(Extraction(value=m.group(), start=m.start(), end=m.end(), pattern="ipv4"))
    for m in _IP_V6_RE.finditer(text):
        results.append(Extraction(value=m.group(), start=m.start(), end=m.end(), pattern="ipv6"))
    return results


def extract_uuids(text: str) -> list[Extraction]:
    """Extract UUIDs (v1-v5) from text.

    Args:
        text: Input text.

    Returns:
        List of Extraction objects with UUID values and positions.
    """
    return [Extraction(value=m.group(), start=m.start(), end=m.end(), pattern="uuid") for m in _UUID_RE.finditer(text)]


def extract_dates(text: str) -> list[Extraction]:
    """Extract dates from text in various formats.

    Supported formats:
    - YYYY-MM-DD, YYYY/MM/DD, YYYY.MM.DD
    - DD-MM-YYYY, DD/MM/YYYY, DD.MM.YYYY
    - DD Month YYYY (e.g., "15 January 2024")
    - Month DD, YYYY (e.g., "January 15, 2024")

    Args:
        text: Input text.

    Returns:
        List of Extraction objects with date values and positions.
    """
    return [Extraction(value=m.group(), start=m.start(), end=m.end(), pattern="date") for m in _DATE_RE.finditer(text)]


def extract_hex_colors(text: str) -> list[Extraction]:
    """Extract hex color codes from text.

    Supports both 3-digit (#RGB) and 6-digit (#RRGGBB) formats,
    with # or 0x prefix.

    Args:
        text: Input text.

    Returns:
        List of Extraction objects with hex color values and positions.
    """
    return [
        Extraction(value=m.group(), start=m.start(), end=m.end(), pattern="hex_color")
        for m in _HEX_COLOR_RE.finditer(text)
    ]


def extract_all(text: str) -> list[Extraction]:
    """Extract all recognized patterns from text.

    Runs all extractors and returns results sorted by position.

    Args:
        text: Input text.

    Returns:
        List of Extraction objects sorted by start position.
    """
    results = []
    results.extend(extract_emails(text))
    results.extend(extract_urls(text))
    results.extend(extract_phone_numbers(text))
    results.extend(extract_ip_addresses(text))
    results.extend(extract_uuids(text))
    results.extend(extract_dates(text))
    results.extend(extract_hex_colors(text))
    results.sort(key=lambda e: e.start)
    return results
