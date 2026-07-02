"""String similarity algorithms."""

from __future__ import annotations

import math
from collections import Counter


def levenshtein_distance(s1: str, s2: str) -> int:
    """Compute the Levenshtein edit distance between two strings.

    Uses dynamic programming with O(min(m,n)) space.
    Operations: insert, delete, substitute — each costs 1.

    Args:
        s1: First string.
        s2: Second string.

    Returns:
        Minimum number of single-character edits to transform s1 into s2.
    """
    if s1 == s2:
        return 0
    if not s1:
        return len(s2)
    if not s2:
        return len(s1)

    # Optimize: ensure s2 is the shorter string for space
    if len(s1) < len(s2):
        s1, s2 = s2, s1

    prev = list(range(len(s2) + 1))
    curr = [0] * (len(s2) + 1)

    for i in range(1, len(s1) + 1):
        curr[0] = i
        for j in range(1, len(s2) + 1):
            cost = 0 if s1[i - 1] == s2[j - 1] else 1
            curr[j] = min(
                prev[j] + 1,  # deletion
                curr[j - 1] + 1,  # insertion
                prev[j - 1] + cost,  # substitution
            )
        prev, curr = curr, prev

    return prev[len(s2)]


def damerau_levenshtein_distance(s1: str, s2: str) -> int:
    """Compute the Damerau-Levenshtein distance (includes transposition).

    Extends Levenshtein with adjacent character transposition as a single operation.

    Args:
        s1: First string.
        s2: Second string.

    Returns:
        Minimum number of operations (insert, delete, substitute, transpose) to transform s1 into s2.
    """
    if s1 == s2:
        return 0
    if not s1:
        return len(s2)
    if not s2:
        return len(s1)

    len1, len2 = len(s1), len(s2)
    # Use a matrix for the DP
    d = [[0] * (len2 + 1) for _ in range(len1 + 1)]

    for i in range(len1 + 1):
        d[i][0] = i
    for j in range(len2 + 1):
        d[0][j] = j

    for i in range(1, len1 + 1):
        for j in range(1, len2 + 1):
            cost = 0 if s1[i - 1] == s2[j - 1] else 1
            d[i][j] = min(
                d[i - 1][j] + 1,  # deletion
                d[i][j - 1] + 1,  # insertion
                d[i - 1][j - 1] + cost,  # substitution
            )
            # Transposition
            if i > 1 and j > 1 and s1[i - 1] == s2[j - 2] and s1[i - 2] == s2[j - 1]:
                d[i][j] = min(d[i][j], d[i - 2][j - 2] + 1)

    return d[len1][len2]


def jaro_similarity(s1: str, s2: str) -> float:
    """Compute the Jaro similarity between two strings.

    Returns a value between 0.0 (no similarity) and 1.0 (identical).
    Based on the number and order of matching characters plus transpositions.

    Args:
        s1: First string.
        s2: Second string.

    Returns:
        Jaro similarity score in [0.0, 1.0].
    """
    if s1 == s2:
        return 1.0
    if not s1 or not s2:
        return 0.0

    len1, len2 = len(s1), len(s2)
    match_distance = max(len1, len2) // 2 - 1
    match_distance = max(0, match_distance)

    s1_matches = [False] * len1
    s2_matches = [False] * len2

    matches = 0
    transpositions = 0

    for i in range(len1):
        start = max(0, i - match_distance)
        end = min(i + match_distance + 1, len2)
        for j in range(start, end):
            if s2_matches[j] or s1[i] != s2[j]:
                continue
            s1_matches[i] = True
            s2_matches[j] = True
            matches += 1
            break

    if matches == 0:
        return 0.0

    k = 0
    for i in range(len1):
        if not s1_matches[i]:
            continue
        while not s2_matches[k]:
            k += 1
        if s1[i] != s2[k]:
            transpositions += 1
        k += 1

    return (matches / len1 + matches / len2 + (matches - transpositions / 2) / matches) / 3


def jaro_winkler_similarity(s1: str, s2: str, prefix_weight: float = 0.1) -> float:
    """Compute the Jaro-Winkler similarity.

    Boosts the Jaro similarity score for strings that share a common prefix.
    The prefix weight controls how much the prefix contributes (max 0.25).

    Args:
        s1: First string.
        s2: Second string.
        prefix_weight: Weight for the common prefix bonus (default 0.1).

    Returns:
        Jaro-Winkler similarity score in [0.0, 1.0].
    """
    prefix_weight = min(0.25, max(0.0, prefix_weight))
    jaro = jaro_similarity(s1, s2)

    # Find common prefix (up to 4 characters)
    prefix_len = 0
    for i in range(min(len(s1), len(s2), 4)):
        if s1[i] == s2[i]:
            prefix_len += 1
        else:
            break

    return jaro + prefix_len * prefix_weight * (1 - jaro)


def cosine_similarity(s1: str, s2: str) -> float:
    """Compute cosine similarity between two strings using character bigrams.

    Tokenizes strings into character bigrams and computes cosine similarity
    of the resulting frequency vectors.

    Args:
        s1: First string.
        s2: Second string.

    Returns:
        Cosine similarity score in [0.0, 1.0].
    """
    if not s1 or not s2:
        return 0.0

    def _bigrams(s: str) -> Counter:
        return Counter(s[i : i + 2] for i in range(len(s) - 1)) if len(s) > 1 else Counter({s: 1})

    v1 = _bigrams(s1)
    v2 = _bigrams(s2)

    intersection = set(v1.keys()) & set(v2.keys())
    dot_product = sum(v1[k] * v2[k] for k in intersection)

    mag1 = math.sqrt(sum(v * v for v in v1.values()))
    mag2 = math.sqrt(sum(v * v for v in v2.values()))

    if mag1 == 0 or mag2 == 0:
        return 0.0

    return dot_product / (mag1 * mag2)


def jaccard_similarity(s1: str, s2: str) -> float:
    """Compute Jaccard similarity between two strings using character bigrams.

    Args:
        s1: First string.
        s2: Second string.

    Returns:
        Jaccard similarity score in [0.0, 1.0].
    """
    if not s1 or not s2:
        return 0.0

    def _bigrams(s: str) -> set:
        return {s[i : i + 2] for i in range(len(s) - 1)} if len(s) > 1 else {s}

    b1 = _bigrams(s1)
    b2 = _bigrams(s2)

    if not b1 and not b2:
        return 1.0

    intersection = len(b1 & b2)
    union = len(b1 | b2)

    return intersection / union if union > 0 else 0.0


def sorensen_dice_coefficient(s1: str, s2: str) -> float:
    """Compute the Sørensen-Dice coefficient between two strings using bigrams.

    Similar to Jaccard but weights intersection more heavily.
    Score = 2 * |intersection| / (|s1| + |s2|)

    Args:
        s1: First string.
        s2: Second string.

    Returns:
        Dice coefficient in [0.0, 1.0].
    """
    if not s1 or not s2:
        return 0.0

    def _bigrams(s: str) -> set:
        return {s[i : i + 2] for i in range(len(s) - 1)} if len(s) > 1 else {s}

    b1 = _bigrams(s1)
    b2 = _bigrams(s2)

    if not b1 and not b2:
        return 1.0

    intersection = len(b1 & b2)
    return 2.0 * intersection / (len(b1) + len(b2))


def hamming_distance(s1: str, s2: str) -> int:
    """Compute the Hamming distance between two strings.

    Counts the number of positions where characters differ.
    Strings must be the same length.

    Args:
        s1: First string.
        s2: Second string.

    Returns:
        Number of differing positions.

    Raises:
        ValueError: If strings have different lengths.
    """
    if len(s1) != len(s2):
        raise ValueError(f"Strings must have equal length: {len(s1)} != {len(s2)}")
    return sum(c1 != c2 for c1, c2 in zip(s1, s2, strict=True))


def normalized_levenshtein(s1: str, s2: str) -> float:
    """Compute normalized Levenshtein distance (0.0 = identical, 1.0 = completely different).

    Args:
        s1: First string.
        s2: Second string.

    Returns:
        Normalized distance in [0.0, 1.0].
    """
    max_len = max(len(s1), len(s2))
    if max_len == 0:
        return 0.0
    return levenshtein_distance(s1, s2) / max_len
