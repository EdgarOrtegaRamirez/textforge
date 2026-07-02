"""Text chunking algorithms for splitting text into manageable pieces."""

from __future__ import annotations

import re


def chunk_by_sentences(text: str, max_chunk_size: int = 500) -> list[str]:
    """Split text into chunks by sentences, respecting max size.

    Splits on sentence boundaries (.!?) and groups sentences into chunks
    that don't exceed max_chunk_size characters.

    Args:
        text: Input text.
        max_chunk_size: Maximum characters per chunk (default 500).

    Returns:
        List of text chunks.
    """
    if not text.strip():
        return []

    # Split on sentence boundaries, keeping the delimiter
    sentences = re.split(r"(?<=[.!?])\s+", text.strip())
    return _group_into_chunks(sentences, max_chunk_size)


def chunk_by_paragraphs(text: str, max_chunk_size: int = 1000) -> list[str]:
    """Split text into chunks by paragraphs.

    Paragraphs are separated by blank lines.

    Args:
        text: Input text.
        max_chunk_size: Maximum characters per chunk (default 1000).

    Returns:
        List of text chunks.
    """
    if not text.strip():
        return []

    paragraphs = re.split(r"\n\s*\n", text.strip())
    paragraphs = [p.strip() for p in paragraphs if p.strip()]
    return _group_into_chunks(paragraphs, max_chunk_size)


def chunk_by_words(text: str, words_per_chunk: int = 100) -> list[str]:
    """Split text into chunks by word count.

    Args:
        text: Input text.
        words_per_chunk: Number of words per chunk (default 100).

    Returns:
        List of text chunks.
    """
    if not text.strip():
        return []

    words = text.split()
    chunks = []
    for i in range(0, len(words), words_per_chunk):
        chunk_words = words[i : i + words_per_chunk]
        chunks.append(" ".join(chunk_words))
    return chunks


def chunk_by_characters(text: str, chars_per_chunk: int = 1000) -> list[str]:
    """Split text into chunks by character count.

    Attempts to break at word boundaries.

    Args:
        text: Input text.
        chars_per_chunk: Number of characters per chunk (default 1000).

    Returns:
        List of text chunks.
    """
    if not text:
        return []

    chunks = []
    while text:
        if len(text) <= chars_per_chunk:
            chunks.append(text)
            break

        # Find a good break point
        break_point = text.rfind(" ", 0, chars_per_chunk)
        if break_point <= chars_per_chunk // 2:
            break_point = chars_per_chunk

        chunks.append(text[:break_point])
        text = text[break_point:].lstrip()

    return chunks


def chunk_with_overlap(
    text: str,
    chunk_size: int = 500,
    overlap: int = 50,
    by: str = "words",
) -> list[str]:
    """Split text into overlapping chunks.

    Useful for RAG pipelines where context needs to span chunk boundaries.

    Args:
        text: Input text.
        chunk_size: Size of each chunk (in words or characters).
        overlap: Number of words/characters to overlap between chunks.
        by: Unit of chunking — "words" or "chars".

    Returns:
        List of overlapping text chunks.
    """
    if not text.strip():
        return []

    tokens = text.split() if by == "words" else list(text)

    if chunk_size >= len(tokens):
        return [text]

    chunks = []
    step = chunk_size - overlap

    for i in range(0, len(tokens), step):
        chunk_tokens = tokens[i : i + chunk_size]
        if not chunk_tokens:
            break
        if by == "words":
            chunks.append(" ".join(chunk_tokens))
        else:
            chunks.append("".join(chunk_tokens))

    return chunks


def _group_into_chunks(items: list[str], max_size: int) -> list[str]:
    """Group text items into chunks that don't exceed max_size characters."""
    if not items:
        return []

    chunks = []
    current_chunk: list[str] = []
    current_size = 0

    for item in items:
        item_size = len(item)
        if current_size + item_size + (1 if current_chunk else 0) <= max_size:
            current_chunk.append(item)
            current_size += item_size + (1 if len(current_chunk) > 1 else 0)
        else:
            if current_chunk:
                chunks.append(" ".join(current_chunk))
            # If a single item exceeds max_size, add it as its own chunk
            if item_size > max_size:
                chunks.append(item)
                current_chunk = []
                current_size = 0
            else:
                current_chunk = [item]
                current_size = item_size

    if current_chunk:
        chunks.append(" ".join(current_chunk))

    return chunks
