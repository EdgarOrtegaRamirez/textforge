"""Text validation functions for common formats."""

from __future__ import annotations

import re
from datetime import datetime


def is_valid_email(email: str) -> bool:
    """Validate an email address.

    Checks basic format: local@domain.tld
    - Local part: alphanumeric, dots, hyphens, underscores, plus signs
    - Domain: alphanumeric, hyphens, dots
    - TLD: at least 2 characters

    Args:
        email: The email address to validate.

    Returns:
        True if the email appears valid, False otherwise.
    """
    pattern = re.compile(r"^[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9\-]+(?:\.[a-zA-Z0-9\-]+)*\.[a-zA-Z]{2,}$")
    return bool(pattern.match(email))


def is_valid_url(url: str) -> bool:
    """Validate a URL.

    Checks for http:// or https:// scheme, valid domain, and optional path.

    Args:
        url: The URL to validate.

    Returns:
        True if the URL appears valid, False otherwise.
    """
    pattern = re.compile(
        r"^https?://"
        r"(?:[a-zA-Z0-9\-]+\.)*[a-zA-Z0-9\-]+\.[a-zA-Z]{2,}"
        r"(?::\d{1,5})?"
        r"(?:/[^\s]*)?$"
    )
    return bool(pattern.match(url))


def is_valid_ip_address(ip: str) -> bool:
    """Validate an IPv4 or IPv6 address.

    Args:
        ip: The IP address to validate.

    Returns:
        True if the IP address is valid, False otherwise.
    """
    # Try IPv4
    parts = ip.split(".")
    if len(parts) == 4:
        try:
            return all(0 <= int(part) <= 255 and part == str(int(part)) for part in parts)
        except ValueError:
            pass

    # Try IPv6 (simplified validation)
    if ":" in ip:
        parts = ip.split(":")
        if len(parts) == 8:
            return all(re.match(r"^[0-9a-fA-F]{1,4}$", part) for part in parts)
        # Check for :: compression
        if "::" in ip:
            # Allow empty parts around ::
            parts = ip.split("::")
            if len(parts) == 2:
                left = [p for p in parts[0].split(":") if p]
                right = [p for p in parts[1].split(":") if p]
                total = len(left) + len(right)
                return total <= 7 and all(re.match(r"^[0-9a-fA-F]{1,4}$", p) for p in left + right)

    return False


def is_valid_uuid(uuid_str: str) -> bool:
    """Validate a UUID (v1-v5).

    Args:
        uuid_str: The UUID string to validate.

    Returns:
        True if the UUID format is valid, False otherwise.
    """
    pattern = re.compile(
        r"^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}"
        r"-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$"
    )
    return bool(pattern.match(uuid_str))


def is_valid_hex_color(color: str) -> bool:
    """Validate a hex color code.

    Supports 3-digit (#RGB) and 6-digit (#RRGGBB) formats.

    Args:
        color: The hex color string to validate.

    Returns:
        True if the color code is valid, False otherwise.
    """
    pattern = re.compile(r"^#(?:[0-9a-fA-F]{3}){1,2}$")
    return bool(pattern.match(color))


def is_valid_date(date_str: str) -> bool:
    """Validate a date string in common formats.

    Supported formats:
    - YYYY-MM-DD
    - YYYY/MM/DD
    - DD-MM-YYYY
    - DD/MM/YYYY
    - MM/DD/YYYY
    - YYYYMMDD

    Args:
        date_str: The date string to validate.

    Returns:
        True if the date is valid, False otherwise.
    """
    formats = [
        "%Y-%m-%d",
        "%Y/%m/%d",
        "%d-%m-%Y",
        "%d/%m/%Y",
        "%m/%d/%Y",
        "%Y%m%d",
    ]
    for fmt in formats:
        try:
            datetime.strptime(date_str.strip(), fmt)
            return True
        except ValueError:
            continue
    return False


def is_valid_isbn(isbn: str) -> bool:
    """Validate an ISBN-10 or ISBN-13 number.

    Validates both the format and the check digit.

    Args:
        isbn: The ISBN string to validate.

    Returns:
        True if the ISBN is valid, False otherwise.
    """
    cleaned = isbn.replace("-", "").replace(" ", "")

    # ISBN-13
    if len(cleaned) == 13 and cleaned.isdigit():
        total = sum(int(d) * (1 if i % 2 == 0 else 3) for i, d in enumerate(cleaned))
        return total % 10 == 0

    # ISBN-10
    if len(cleaned) == 10:
        total = 0
        for i, char in enumerate(cleaned[:-1]):
            if not char.isdigit():
                return False
            total += int(char) * (10 - i)
        check = cleaned[-1]
        if check == "X" or check == "x":
            total += 10
        elif check.isdigit():
            total += int(check)
        else:
            return False
        return total % 11 == 0

    return False


def is_valid_semver(version: str) -> bool:
    """Validate a Semantic Version string (MAJOR.MINOR.PATCH).

    Optionally supports pre-release and build metadata:
    - 1.0.0
    - 1.0.0-beta.1
    - 1.0.0+build.123
    - 1.0.0-alpha+001

    Args:
        version: The version string to validate.

    Returns:
        True if the version is valid semver, False otherwise.
    """
    pattern = re.compile(
        r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)"
        r"(?:-((?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)"
        r"(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?"
        r"(?:\+([0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?$"
    )
    return bool(pattern.match(version))


def is_valid_json(value: str) -> bool:
    """Validate whether a string is valid JSON.

    Args:
        value: The string to validate.

    Returns:
        True if the string is valid JSON, False otherwise.
    """
    import json

    try:
        json.loads(value)
        return True
    except (json.JSONDecodeError, ValueError):
        return False
