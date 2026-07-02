"""Tests for textforge.statistics module."""

from textforge.statistics import (
    average_sentence_length,
    average_word_length,
    character_density,
    character_frequency,
    hapax_legomena_ratio,
    lexical_density,
    paragraph_count,
    readability_score,
    sentence_count,
    shannon_entropy,
    type_token_ratio,
    word_count,
)


class TestWordCount:
    def test_basic(self):
        assert word_count("hello world") == 2

    def test_empty(self):
        assert word_count("") == 0

    def test_whitespace_only(self):
        assert word_count("   \n\t  ") == 0

    def test_single_word(self):
        assert word_count("hello") == 1

    def test_multiple_spaces(self):
        assert word_count("hello   world") == 2


class TestSentenceCount:
    def test_basic(self):
        assert sentence_count("Hello world.") == 1

    def test_multiple(self):
        assert sentence_count("Hello world. How are you? Fine!") == 3

    def test_empty(self):
        assert sentence_count("") == 0

    def test_no_punctuation(self):
        assert sentence_count("hello world") >= 1


class TestParagraphCount:
    def test_single(self):
        assert paragraph_count("hello world") == 1

    def test_multiple(self):
        assert paragraph_count("para 1\n\npara 2\n\npara 3") == 3

    def test_empty(self):
        assert paragraph_count("") == 0

    def test_blank_lines(self):
        assert paragraph_count("a\n\n\n\nb") == 2


class TestCharacterFrequency:
    def test_basic(self):
        freq = character_frequency("aab")
        assert freq["a"] == 2
        assert freq["b"] == 1

    def test_case_insensitive(self):
        freq = character_frequency("AaB", ignore_case=True)
        assert freq["a"] == 2

    def test_ignore_spaces(self):
        freq = character_frequency("a b", ignore_spaces=True)
        assert " " not in freq

    def test_empty(self):
        assert character_frequency("") == {}


class TestShannonEntropy:
    def test_empty(self):
        assert shannon_entropy("") == 0.0

    def test_single_char(self):
        assert shannon_entropy("aaa") == 0.0

    def test_uniform(self):
        # Two characters, each appearing once
        entropy = shannon_entropy("ab")
        assert abs(entropy - 1.0) < 0.01

    def test_range(self):
        entropy = shannon_entropy("hello world")
        assert 0.0 < entropy < 10.0


class TestReadabilityScore:
    def test_basic(self):
        text = "The quick brown fox jumps over the lazy dog. This is a simple sentence."
        result = readability_score(text)
        assert "flesch_ease" in result
        assert "flesch_kincaid_grade" in result
        assert "total_words" in result
        assert result["total_words"] > 0

    def test_empty(self):
        result = readability_score("")
        assert result["total_words"] == 0

    def test_simple_text(self):
        result = readability_score("The cat sat on the mat.")
        assert result["flesch_ease"] > 0


class TestAverageWordLength:
    def test_basic(self):
        assert average_word_length("hi ok") == 2.0

    def test_empty(self):
        assert average_word_length("") == 0.0

    def test_single_word(self):
        assert average_word_length("hello") == 5.0


class TestAverageSentenceLength:
    def test_basic(self):
        result = average_sentence_length("Hello world. How are you?")
        assert result > 0

    def test_empty(self):
        assert average_sentence_length("") == 0.0


class TestTypeTokenRatio:
    def test_identical_words(self):
        assert type_token_ratio("the the the") == 1 / 3

    def test_all_unique(self):
        assert type_token_ratio("a b c d") == 1.0

    def test_empty(self):
        assert type_token_ratio("") == 0.0


class TestHapaxLegomenaRatio:
    def test_all_unique(self):
        assert hapax_legomena_ratio("a b c") == 1.0

    def test_all_repeated(self):
        assert hapax_legomena_ratio("the the the") == 0.0

    def test_empty(self):
        assert hapax_legomena_ratio("") == 0.0


class TestCharacterDensity:
    def test_basic(self):
        result = character_density("Hello 123!")
        assert result["letters"] > 0
        assert result["digits"] > 0
        assert result["punctuation"] > 0

    def test_empty(self):
        result = character_density("")
        assert all(v == 0.0 for v in result.values())


class TestLexicalDensity:
    def test_content_heavy(self):
        result = lexical_density("Big brown fox jumps quickly.")
        assert result > 0.3

    def test_function_words(self):
        result = lexical_density("the a an is are was")
        assert result < 0.3

    def test_empty(self):
        assert lexical_density("") == 0.0
