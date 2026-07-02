"""Text statistics and analysis algorithms."""

from __future__ import annotations

import math
import re
from collections import Counter


def word_count(text: str) -> int:
    """Count the number of words in text.

    A word is defined as a sequence of non-whitespace characters separated by whitespace.

    Args:
        text: Input text.

    Returns:
        Number of words.
    """
    return len(text.split())


def sentence_count(text: str) -> int:
    """Count the number of sentences in text.

    Sentences are delimited by sentence-ending punctuation (. ! ?)
    with optional whitespace. Handles edge cases like abbreviations.

    Args:
        text: Input text.

    Returns:
        Number of sentences.
    """
    if not text.strip():
        return 0
    # Split on sentence-ending punctuation followed by whitespace or end of string
    # Avoid splitting on common abbreviations (Mr., Mrs., Dr., etc.)
    abbrevs = re.compile(r"\b(?:Mr|Mrs|Ms|Dr|Prof|Sr|Jr|St|vs|etc|Inc|Ltd|Corp|vs|al)\.", re.IGNORECASE)
    cleaned = abbrevs.sub(lambda m: m.group().replace(".", "<DOT>"), text)
    sentences = re.split(r"[.!?]+(?:\s|$)", cleaned)
    return max(1, len([s for s in sentences if s.strip()]))


def paragraph_count(text: str) -> int:
    """Count the number of paragraphs in text.

    Paragraphs are separated by one or more blank lines.

    Args:
        text: Input text.

    Returns:
        Number of paragraphs.
    """
    if not text.strip():
        return 0
    paragraphs = re.split(r"\n\s*\n", text.strip())
    return len([p for p in paragraphs if p.strip()])


def character_frequency(text: str, ignore_case: bool = True, ignore_spaces: bool = True) -> dict[str, int]:
    """Compute character frequency distribution.

    Args:
        text: Input text.
        ignore_case: If True, treat all characters as lowercase.
        ignore_spaces: If True, ignore whitespace characters.

    Returns:
        Dictionary mapping characters to their frequency counts, sorted by count descending.
    """
    if ignore_case:
        text = text.lower()
    if ignore_spaces:
        text = re.sub(r"\s+", "", text)
    freq = Counter(text)
    return dict(freq.most_common())


def shannon_entropy(text: str) -> float:
    """Compute the Shannon entropy of text in bits per character.

    Higher entropy indicates more randomness/unpredictability.
    - English text: ~4.0-4.5 bits/char
    - Random ASCII: ~6.0-7.0 bits/char
    - Repetitive text: ~1.0-2.0 bits/char

    Args:
        text: Input text.

    Returns:
        Shannon entropy in bits per character.
    """
    if not text:
        return 0.0
    freq = Counter(text)
    length = len(text)
    entropy = 0.0
    for count in freq.values():
        p = count / length
        if p > 0:
            entropy -= p * math.log2(p)
    return entropy


def character_density(text: str) -> dict[str, float]:
    """Compute the density of character categories in text.

    Returns the proportion of characters in each category:
    - letters: alphabetic characters
    - digits: numeric characters
    - spaces: whitespace characters
    - punctuation: punctuation characters
    - other: all other characters

    Args:
        text: Input text.

    Returns:
        Dictionary mapping category names to proportions (0.0-1.0).
    """
    if not text:
        return {"letters": 0.0, "digits": 0.0, "spaces": 0.0, "punctuation": 0.0, "other": 0.0}

    total = len(text)
    return {
        "letters": sum(c.isalpha() for c in text) / total,
        "digits": sum(c.isdigit() for c in text) / total,
        "spaces": sum(c.isspace() for c in text) / total,
        "punctuation": sum(not c.isalnum() and not c.isspace() for c in text) / total,
        "other": 0.0,  # All chars are covered by the above categories
    }


def readability_score(text: str) -> dict[str, float]:
    """Compute readability scores for text.

    Implements the Flesch Reading Ease and Flesch-Kincaid Grade Level formulas.

    Flesch Reading Ease:
        206.835 - 1.015 * (total_words / total_sentences) - 84.6 * (total_syllables / total_words)
        - 90-100: Very Easy
        - 80-89: Easy
        - 70-79: Fairly Easy
        - 60-69: Standard
        - 50-59: Fairly Difficult
        - 30-49: Difficult
        - 0-29: Very Confusing

    Flesch-Kincaid Grade Level:
        0.39 * (total_words / total_sentences) + 11.8 * (total_syllables / total_words) - 15.59

    Args:
        text: Input text.

    Returns:
        Dictionary with 'flesch_ease', 'flesch_kincaid_grade', 'avg_words_per_sentence',
        'avg_syllables_per_word', 'total_words', 'total_sentences'.
    """
    words = text.split()
    total_words = len(words)
    total_sentences = sentence_count(text)
    total_syllables = sum(_count_syllables(w) for w in words)

    if total_words == 0 or total_sentences == 0:
        return {
            "flesch_ease": 0.0,
            "flesch_kincaid_grade": 0.0,
            "avg_words_per_sentence": 0.0,
            "avg_syllables_per_word": 0.0,
            "total_words": 0,
            "total_sentences": 0,
        }

    avg_words_per_sentence = total_words / total_sentences
    avg_syllables_per_word = total_syllables / total_words

    flesch_ease = 206.835 - 1.015 * avg_words_per_sentence - 84.6 * avg_syllables_per_word
    flesch_kincaid = 0.39 * avg_words_per_sentence + 11.8 * avg_syllables_per_word - 15.59

    return {
        "flesch_ease": round(flesch_ease, 2),
        "flesch_kincaid_grade": round(max(0, flesch_kincaid), 2),
        "avg_words_per_sentence": round(avg_words_per_sentence, 2),
        "avg_syllables_per_word": round(avg_syllables_per_word, 2),
        "total_words": total_words,
        "total_sentences": total_sentences,
    }


def average_word_length(text: str) -> float:
    """Compute the average word length in characters.

    Args:
        text: Input text.

    Returns:
        Average word length. Returns 0.0 for empty text.
    """
    words = text.split()
    if not words:
        return 0.0
    return sum(len(w) for w in words) / len(words)


def average_sentence_length(text: str) -> float:
    """Compute the average sentence length in words.

    Args:
        text: Input text.

    Returns:
        Average words per sentence. Returns 0.0 for empty text.
    """
    sents = sentence_count(text)
    if sents == 0:
        return 0.0
    return word_count(text) / sents


def type_token_ratio(text: str) -> float:
    """Compute the Type-Token Ratio (TTR) — lexical diversity.

    TTR = unique_words / total_words. Higher values indicate more diverse vocabulary.

    Args:
        text: Input text.

    Returns:
        TTR in [0.0, 1.0].
    """
    words = text.lower().split()
    if not words:
        return 0.0
    return len(set(words)) / len(words)


def hapax_legomena_ratio(text: str) -> float:
    """Compute the ratio of words that appear exactly once (hapax legomena).

    Higher ratio indicates more unique vocabulary usage.

    Args:
        text: Input text.

    Returns:
        Ratio of unique words to total words in [0.0, 1.0].
    """
    words = text.lower().split()
    if not words:
        return 0.0
    freq = Counter(words)
    hapax = sum(1 for count in freq.values() if count == 1)
    return hapax / len(words)


def _count_syllables(word: str) -> int:
    """Estimate syllable count for an English word.

    Uses a vowel-group heuristic: count groups of consecutive vowels,
    adjust for silent-e and common patterns.

    Args:
        word: A single word.

    Returns:
        Estimated number of syllables (minimum 1).
    """
    word = word.lower().strip()
    if not word:
        return 0
    if len(word) <= 3:
        return 1

    # Count vowel groups
    vowels = "aeiouy"
    count = 0
    prev_vowel = False
    for char in word:
        is_vowel = char in vowels
        if is_vowel and not prev_vowel:
            count += 1
        prev_vowel = is_vowel

    # Adjust for silent-e
    if word.endswith("e") and not word.endswith("le") and count > 1:
        count -= 1

    # Adjust for common patterns
    if word.endswith("ed") and not word.endswith("ted") and not word.endswith("ded") and count > 1:
        count -= 1

    return max(1, count)


def lexical_density(text: str) -> float:
    """Compute lexical density — ratio of content words to total words.

    Content words: nouns, verbs, adjectives, adverbs (approximated by excluding
    common stop words).

    Args:
        text: Input text.

    Returns:
        Lexical density in [0.0, 1.0].
    """
    # Common English stop words
    stop_words = {
        "a",
        "an",
        "the",
        "and",
        "or",
        "but",
        "in",
        "on",
        "at",
        "to",
        "for",
        "of",
        "with",
        "by",
        "from",
        "as",
        "is",
        "was",
        "are",
        "were",
        "be",
        "been",
        "being",
        "have",
        "has",
        "had",
        "do",
        "does",
        "did",
        "will",
        "would",
        "could",
        "should",
        "may",
        "might",
        "shall",
        "can",
        "need",
        "dare",
        "ought",
        "used",
        "it",
        "its",
        "he",
        "she",
        "they",
        "them",
        "his",
        "her",
        "their",
        "this",
        "that",
        "these",
        "those",
        "i",
        "me",
        "my",
        "we",
        "us",
        "our",
        "you",
        "your",
        "not",
        "no",
        "if",
        "then",
        "than",
        "too",
        "very",
        "so",
        "just",
        "about",
        "also",
        "how",
        "what",
        "when",
        "where",
        "who",
        "which",
        "why",
        "all",
        "each",
        "every",
        "both",
        "few",
        "more",
        "most",
        "other",
        "some",
        "such",
        "only",
        "own",
        "same",
        "here",
        "there",
        "up",
        "out",
        "off",
        "over",
        "under",
        "again",
        "further",
        "once",
    }
    words = text.lower().split()
    if not words:
        return 0.0
    content_words = [w for w in words if w.strip(".,!?;:'\"()-") not in stop_words]
    return len(content_words) / len(words)
