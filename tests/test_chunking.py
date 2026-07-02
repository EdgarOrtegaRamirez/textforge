"""Tests for textforge.chunking module."""

from textforge.chunking import (
    chunk_by_characters,
    chunk_by_paragraphs,
    chunk_by_sentences,
    chunk_by_words,
    chunk_with_overlap,
)


class TestChunkBySentences:
    def test_single_sentence(self):
        chunks = chunk_by_sentences("Hello world.")
        assert len(chunks) == 1
        assert "Hello world." in chunks[0]

    def test_multiple_sentences(self):
        text = "First sentence. Second sentence. Third sentence."
        chunks = chunk_by_sentences(text, max_chunk_size=30)
        assert len(chunks) >= 2

    def test_empty(self):
        assert chunk_by_sentences("") == []
        assert chunk_by_sentences("   ") == []

    def test_small_chunks(self):
        text = "A. B. C. D. E."
        chunks = chunk_by_sentences(text, max_chunk_size=5)
        assert len(chunks) >= 3


class TestChunkByParagraphs:
    def test_single_paragraph(self):
        chunks = chunk_by_paragraphs("Hello world")
        assert len(chunks) == 1

    def test_multiple_paragraphs(self):
        text = (
            "This is paragraph one with some text.\n\n"
            "This is paragraph two with more text.\n\n"
            "And this is paragraph three."
        )
        chunks = chunk_by_paragraphs(text, max_chunk_size=40)
        assert len(chunks) >= 2

    def test_empty(self):
        assert chunk_by_paragraphs("") == []


class TestChunkByWords:
    def test_basic(self):
        text = "word1 word2 word3 word4 word5"
        chunks = chunk_by_words(text, words_per_chunk=2)
        assert len(chunks) == 3
        assert chunks[0] == "word1 word2"

    def test_single_chunk(self):
        text = "one two"
        chunks = chunk_by_words(text, words_per_chunk=10)
        assert len(chunks) == 1

    def test_empty(self):
        assert chunk_by_words("") == []


class TestChunkByCharacters:
    def test_basic(self):
        text = "hello world foo bar"
        chunks = chunk_by_characters(text, chars_per_chunk=10)
        for chunk in chunks:
            assert len(chunk) <= 15  # Allow some overflow for word boundaries

    def test_empty(self):
        assert chunk_by_characters("") == []

    def test_single_chunk(self):
        text = "short"
        chunks = chunk_by_characters(text, chars_per_chunk=100)
        assert len(chunks) == 1


class TestChunkWithOverlap:
    def test_basic(self):
        text = " ".join(f"word{i}" for i in range(20))
        chunks = chunk_with_overlap(text, chunk_size=5, overlap=2, by="words")
        assert len(chunks) >= 3
        # Each chunk should have at most 5 words
        for chunk in chunks:
            assert len(chunk.split()) <= 5

    def test_no_overlap(self):
        text = " ".join(f"word{i}" for i in range(10))
        chunks = chunk_with_overlap(text, chunk_size=5, overlap=0, by="words")
        assert len(chunks) == 2

    def test_char_mode(self):
        text = "hello world foo bar baz"
        chunks = chunk_with_overlap(text, chunk_size=10, overlap=3, by="chars")
        assert len(chunks) >= 2

    def test_empty(self):
        assert chunk_with_overlap("") == []
        assert chunk_with_overlap("   ") == []

    def test_small_text(self):
        text = "short"
        chunks = chunk_with_overlap(text, chunk_size=100, overlap=10, by="words")
        assert len(chunks) == 1
