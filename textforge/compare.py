"""Text comparison and diff algorithms."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class DiffOp(Enum):
    """Diff operation type."""

    EQUAL = "equal"
    INSERT = "insert"
    DELETE = "delete"
    REPLACE = "replace"


@dataclass(frozen=True)
class DiffItem:
    """A single diff operation."""

    op: DiffOp
    value: str
    old_pos: int = 0
    new_pos: int = 0

    def __repr__(self) -> str:
        prefix = {"equal": " ", "insert": "+", "delete": "-", "replace": "~"}
        return f"{prefix[self.op.value]} {self.value!r}"


def diff_chars(s1: str, s2: str) -> list[DiffItem]:
    """Compute character-level diff between two strings using LCS.

    Uses the classic LCS (Longest Common Subsequence) dynamic programming
    approach to find the optimal alignment.

    Args:
        s1: First string.
        s2: Second string.

    Returns:
        List of DiffItem operations to transform s1 into s2.
    """
    m, n = len(s1), len(s2)

    # Build LCS table
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s1[i - 1] == s2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])

    # Backtrack to find diff
    result = []
    i, j = m, n
    while i > 0 or j > 0:
        if i > 0 and j > 0 and s1[i - 1] == s2[j - 1]:
            result.append(DiffItem(op=DiffOp.EQUAL, value=s1[i - 1], old_pos=i - 1, new_pos=j - 1))
            i -= 1
            j -= 1
        elif j > 0 and (i == 0 or dp[i][j - 1] >= dp[i - 1][j]):
            result.append(DiffItem(op=DiffOp.INSERT, value=s2[j - 1], new_pos=j - 1))
            j -= 1
        else:
            result.append(DiffItem(op=DiffOp.DELETE, value=s1[i - 1], old_pos=i - 1))
            i -= 1

    result.reverse()
    return _merge_consecutive(result)


def diff_words(s1: str, s2: str) -> list[DiffItem]:
    """Compute word-level diff between two strings.

    Splits on whitespace and computes LCS-based diff on words.

    Args:
        s1: First string.
        s2: Second string.

    Returns:
        List of DiffItem operations to transform s1 into s2.
    """
    words1 = s1.split()
    words2 = s2.split()

    m, n = len(words1), len(words2)

    # Build LCS table
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if words1[i - 1] == words2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])

    # Backtrack
    result = []
    i, j = m, n
    while i > 0 or j > 0:
        if i > 0 and j > 0 and words1[i - 1] == words2[j - 1]:
            result.append(DiffItem(op=DiffOp.EQUAL, value=words1[i - 1], old_pos=i - 1, new_pos=j - 1))
            i -= 1
            j -= 1
        elif j > 0 and (i == 0 or dp[i][j - 1] >= dp[i - 1][j]):
            result.append(DiffItem(op=DiffOp.INSERT, value=words2[j - 1], new_pos=j - 1))
            j -= 1
        else:
            result.append(DiffItem(op=DiffOp.DELETE, value=words1[i - 1], old_pos=i - 1))
            i -= 1

    result.reverse()
    return result


def diff_lines(s1: str, s2: str) -> list[DiffItem]:
    """Compute line-level diff between two strings.

    Splits on newlines and computes LCS-based diff on lines.

    Args:
        s1: First string.
        s2: Second string.

    Returns:
        List of DiffItem operations to transform s1 into s2.
    """
    lines1 = s1.splitlines(keepends=True)
    lines2 = s2.splitlines(keepends=True)

    m, n = len(lines1), len(lines2)

    # Build LCS table
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if lines1[i - 1] == lines2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])

    # Backtrack
    result = []
    i, j = m, n
    while i > 0 or j > 0:
        if i > 0 and j > 0 and lines1[i - 1] == lines2[j - 1]:
            result.append(DiffItem(op=DiffOp.EQUAL, value=lines1[i - 1], old_pos=i - 1, new_pos=j - 1))
            i -= 1
            j -= 1
        elif j > 0 and (i == 0 or dp[i][j - 1] >= dp[i - 1][j]):
            result.append(DiffItem(op=DiffOp.INSERT, value=lines2[j - 1], new_pos=j - 1))
            j -= 1
        else:
            result.append(DiffItem(op=DiffOp.DELETE, value=lines1[i - 1], old_pos=i - 1))
            i -= 1

    result.reverse()
    return result


def line_similarity(s1: str, s2: str) -> float:
    """Compute line-level similarity between two texts.

    Uses the ratio of common lines to total unique lines.

    Args:
        s1: First text.
        s2: Second text.

    Returns:
        Similarity score in [0.0, 1.0].
    """
    lines1 = set(s1.splitlines())
    lines2 = set(s2.splitlines())

    if not lines1 and not lines2:
        return 1.0
    if not lines1 or not lines2:
        return 0.0

    intersection = len(lines1 & lines2)
    union = len(lines1 | lines2)

    return intersection / union if union > 0 else 0.0


def unified_diff(s1: str, s2: str, context: int = 3) -> str:
    """Generate a unified diff between two strings.

    Args:
        s1: Original text.
        s2: Modified text.
        context: Number of context lines around changes (default 3).

    Returns:
        Unified diff as a string.
    """
    diff = diff_lines(s1, s2)
    if not diff or all(d.op == DiffOp.EQUAL for d in diff):
        return ""

    lines = []
    lines.append("--- original")
    lines.append("+++ modified")

    # Group changes with context
    pending_equal = []

    for item in diff:
        if item.op == DiffOp.EQUAL:
            pending_equal.append(item)
            if len(pending_equal) > context * 2 + 1:
                # Output middle equal lines
                for eq in pending_equal[context:-context]:
                    lines.append(f" {eq.value}")
                pending_equal = pending_equal[-context:]
        else:
            # Flush pending equal lines with context
            for eq in pending_equal[:context]:
                lines.append(f" {eq.value}")
            pending_equal = []

            if item.op == DiffOp.DELETE:
                lines.append(f"-{item.value}")
            elif item.op == DiffOp.INSERT:
                lines.append(f"+{item.value}")
            elif item.op == DiffOp.REPLACE:
                lines.append(f"-{item.value}")

    # Flush remaining
    for eq in pending_equal:
        lines.append(f" {eq.value}")

    return "\n".join(lines)


def _merge_consecutive(items: list[DiffItem]) -> list[DiffItem]:
    """Merge consecutive equal operations into single items."""
    if not items:
        return []

    result = []
    current = items[0]

    for item in items[1:]:
        if item.op == current.op and item.op == DiffOp.EQUAL:
            current = DiffItem(
                op=current.op,
                value=current.value + item.value,
                old_pos=current.old_pos,
                new_pos=current.new_pos,
            )
        else:
            result.append(current)
            current = item

    result.append(current)
    return result
