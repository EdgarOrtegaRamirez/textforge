"""Text transformation functions — case conversion, slugification, normalization."""

from __future__ import annotations

import re
import unicodedata


def to_snake_case(text: str) -> str:
    """Convert text to snake_case.

    Handles camelCase, PascalCase, kebab-case, spaces, and dots.

    Examples:
        >>> to_snake_case("camelCase")
        'camel_case'
        >>> to_snake_case("PascalCase")
        'pascal_case'
        >>> to_snake_case("kebab-case")
        'kebab_case'
        >>> to_snake_case("Hello World")
        'hello_world'

    Args:
        text: Input text.

    Returns:
        snake_case version of the text.
    """
    # Insert underscores before uppercase letters that follow lowercase letters
    text = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", text)
    # Replace non-alphanumeric characters with underscores
    text = re.sub(r"[^a-zA-Z0-9]+", "_", text)
    # Collapse multiple underscores
    text = re.sub(r"_+", "_", text)
    # Strip leading/trailing underscores and convert to lowercase
    return text.strip("_").lower()


def to_camel_case(text: str) -> str:
    """Convert text to camelCase.

    Examples:
        >>> to_camel_case("snake_case")
        'snakeCase'
        >>> to_camel_case("kebab-case")
        'kebabCase'
        >>> to_camel_case("Hello World")
        'helloWorld'

    Args:
        text: Input text.

    Returns:
        camelCase version of the text.
    """
    words = _split_words(text)
    if not words:
        return ""
    return words[0].lower() + "".join(w.capitalize() for w in words[1:])


def to_pascal_case(text: str) -> str:
    """Convert text to PascalCase.

    Examples:
        >>> to_pascal_case("snake_case")
        'SnakeCase'
        >>> to_pascal_case("kebab-case")
        'KebabCase'

    Args:
        text: Input text.

    Returns:
        PascalCase version of the text.
    """
    return "".join(w.capitalize() for w in _split_words(text))


def to_kebab_case(text: str) -> str:
    """Convert text to kebab-case.

    Examples:
        >>> to_kebab_case("camelCase")
        'camel-case'
        >>> to_kebab_case("PascalCase")
        'pascal-case'

    Args:
        text: Input text.

    Returns:
        kebab-case version of the text.
    """
    return "_".join(_split_words(text)).lower().replace("_", "-")


def to_screaming_snake(text: str) -> str:
    """Convert text to SCREAMING_SNAKE_CASE.

    Examples:
        >>> to_screaming_snake("camelCase")
        'CAMEL_CASE'

    Args:
        text: Input text.

    Returns:
        SCREAMING_SNAKE_CASE version of the text.
    """
    return "_".join(_split_words(text)).upper()


def to_dot_case(text: str) -> str:
    """Convert text to dot.case.

    Examples:
        >>> to_dot_case("camelCase")
        'camel.case'
        >>> to_dot_case("snake_case")
        'snake.case'

    Args:
        text: Input text.

    Returns:
        dot.case version of the text.
    """
    return "_".join(_split_words(text)).lower().replace("_", ".")


def to_slug(text: str, separator: str = "-") -> str:
    """Convert text to a URL-friendly slug.

    Normalizes Unicode, removes special characters, and formats with the given separator.

    Examples:
        >>> to_slug("Hello, World!")
        'hello-world'
        >>> to_slug("Café Résumé", separator="_")
        'cafe_resume'

    Args:
        text: Input text.
        separator: Character to use between words (default "-").

    Returns:
        URL-friendly slug.
    """
    # Normalize Unicode (NFKD分解, strip accents)
    text = unicodedata.normalize("NFKD", text)
    text = text.encode("ascii", "ignore").decode("ascii")
    # Replace non-alphanumeric characters with separator
    text = re.sub(r"[^a-zA-Z0-9]+", separator, text)
    # Collapse multiple separators
    text = re.sub(rf"{re.escape(separator)}+", separator, text)
    return text.strip(separator).lower()


def normalize_whitespace(text: str) -> str:
    """Normalize whitespace in text.

    Collapses multiple spaces/tabs into single spaces, trims each line,
    and removes trailing whitespace.

    Args:
        text: Input text.

    Returns:
        Text with normalized whitespace.
    """
    lines = text.split("\n")
    lines = [" ".join(line.split()) for line in lines]
    return "\n".join(lines)


def truncate_text(text: str, max_length: int, suffix: str = "...") -> str:
    """Truncate text to a maximum length, adding a suffix if truncated.

    Tries to break at a word boundary when possible.

    Args:
        text: Input text.
        max_length: Maximum character length (including suffix).
        suffix: String to append when truncated (default "...").

    Returns:
        Truncated text.
    """
    if len(text) <= max_length:
        return text
    if max_length <= len(suffix):
        return text[:max_length]
    truncated = text[: max_length - len(suffix)]
    # Try to break at word boundary
    last_space = truncated.rfind(" ")
    if last_space > max_length // 2:
        truncated = truncated[:last_space]
    return truncated + suffix


def wrap_text(text: str, width: int = 80, indent: str = "") -> str:
    """Wrap text to a specified width.

    Breaks text into lines of at most `width` characters, breaking at word boundaries.

    Args:
        text: Input text.
        width: Maximum line width (default 80).
        indent: String to prepend to each line (default "").

    Returns:
        Wrapped text.
    """
    words = text.split()
    lines = []
    current_line = []
    current_length = len(indent)

    for word in words:
        word_length = len(word)
        if current_length + word_length + (1 if current_line else 0) <= width:
            current_line.append(word)
            current_length += word_length + (1 if len(current_line) > 1 else 0)
        else:
            if current_line:
                lines.append(indent + " ".join(current_line))
            current_line = [word]
            current_length = len(indent) + word_length

    if current_line:
        lines.append(indent + " ".join(current_line))

    return "\n".join(lines)


def dedent_text(text: str) -> str:
    """Remove common leading whitespace from all lines (like textwrap.dedent).

    Args:
        text: Input text.

    Returns:
        Text with common leading whitespace removed.
    """
    import textwrap

    return textwrap.dedent(text)


def title_case(text: str) -> str:
    """Convert text to Title Case with smart capitalization.

    Small words (a, an, the, and, or, etc.) are kept lowercase unless
    they're the first word.

    Args:
        text: Input text.

    Returns:
        Title-cased text.
    """
    small_words = {
        "a",
        "an",
        "the",
        "and",
        "but",
        "or",
        "for",
        "nor",
        "on",
        "at",
        "to",
        "from",
        "by",
        "in",
        "of",
        "with",
        "vs",
        "via",
    }
    words = text.split()
    result = []
    for i, word in enumerate(words):
        if i == 0 or word.lower() not in small_words:
            result.append(word.capitalize())
        else:
            result.append(word.lower())
    return " ".join(result)


def _split_words(text: str) -> list[str]:
    """Split text into words for case conversion.

    Handles camelCase, PascalCase, snake_case, kebab-case, spaces, and dots.
    Filters out empty strings.
    """
    # Insert space before uppercase letters following lowercase/digits
    text = re.sub(r"([a-z0-9])([A-Z])", r"\1 \2", text)
    # Insert space before uppercase letters followed by lowercase (for sequences like "XMLParser")
    text = re.sub(r"([A-Z]+)([A-Z][a-z])", r"\1 \2", text)
    # Replace non-alphanumeric characters with spaces
    text = re.sub(r"[^a-zA-Z0-9]+", " ", text)
    return [w for w in text.split() if w]
