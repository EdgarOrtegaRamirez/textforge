"""Tests for textforge.compare module."""

from textforge.compare import (
    DiffOp,
    diff_chars,
    diff_lines,
    diff_words,
    line_similarity,
    unified_diff,
)


class TestDiffChars:
    def test_identical(self):
        result = diff_chars("abc", "abc")
        assert all(d.op == DiffOp.EQUAL for d in result)
        assert "".join(d.value for d in result) == "abc"

    def test_insertion(self):
        result = diff_chars("ac", "abc")
        ops = [d.op for d in result]
        assert DiffOp.INSERT in ops

    def test_deletion(self):
        result = diff_chars("abc", "ac")
        ops = [d.op for d in result]
        assert DiffOp.DELETE in ops

    def test_empty(self):
        result = diff_chars("", "")
        assert len(result) == 0

    def test_completely_different(self):
        result = diff_chars("abc", "xyz")
        ops = [d.op for d in result]
        assert DiffOp.DELETE in ops
        assert DiffOp.INSERT in ops

    def test_preserves_content(self):
        s1 = "hello"
        s2 = "world"
        result = diff_chars(s1, s2)
        # Reconstruct s2 from diff
        reconstructed = ""
        for d in result:
            if d.op in (DiffOp.EQUAL, DiffOp.INSERT):
                reconstructed += d.value
        assert reconstructed == s2


class TestDiffWords:
    def test_identical(self):
        result = diff_words("hello world", "hello world")
        assert all(d.op == DiffOp.EQUAL for d in result)

    def test_insertion(self):
        result = diff_words("hello", "hello world")
        ops = [d.op for d in result]
        assert DiffOp.INSERT in ops

    def test_deletion(self):
        result = diff_words("hello world", "hello")
        ops = [d.op for d in result]
        assert DiffOp.DELETE in ops


class TestDiffLines:
    def test_identical(self):
        result = diff_lines("line1\nline2", "line1\nline2")
        assert all(d.op == DiffOp.EQUAL for d in result)

    def test_added_line(self):
        result = diff_lines("line1", "line1\nline2")
        ops = [d.op for d in result]
        assert DiffOp.INSERT in ops

    def test_removed_line(self):
        result = diff_lines("line1\nline2", "line1")
        ops = [d.op for d in result]
        assert DiffOp.DELETE in ops

    def test_empty(self):
        result = diff_lines("", "")
        assert len(result) == 0


class TestLineSimilarity:
    def test_identical(self):
        assert line_similarity("hello\nworld", "hello\nworld") == 1.0

    def test_empty(self):
        assert line_similarity("", "") == 1.0

    def test_no_overlap(self):
        assert line_similarity("aaa", "bbb") == 0.0

    def test_partial(self):
        score = line_similarity("aaa\nbbb", "aaa\nccc")
        assert 0.0 < score < 1.0


class TestUnifiedDiff:
    def test_identical(self):
        result = unified_diff("hello", "hello")
        assert result == ""

    def test_different(self):
        result = unified_diff("hello", "world")
        assert "---" in result
        assert "+++" in result
