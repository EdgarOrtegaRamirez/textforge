"""Tests for textforge.similarity module."""

import pytest

from textforge.similarity import (
    cosine_similarity,
    damerau_levenshtein_distance,
    hamming_distance,
    jaccard_similarity,
    jaro_similarity,
    jaro_winkler_similarity,
    levenshtein_distance,
    normalized_levenshtein,
    sorensen_dice_coefficient,
)


class TestLevenshteinDistance:
    def test_identical_strings(self):
        assert levenshtein_distance("hello", "hello") == 0

    def test_empty_strings(self):
        assert levenshtein_distance("", "") == 0
        assert levenshtein_distance("abc", "") == 3
        assert levenshtein_distance("", "abc") == 3

    def test_single_insertion(self):
        assert levenshtein_distance("cat", "cats") == 1

    def test_single_deletion(self):
        assert levenshtein_distance("cats", "cat") == 1

    def test_single_substitution(self):
        assert levenshtein_distance("cat", "bat") == 1

    def test_classic_example(self):
        assert levenshtein_distance("kitten", "sitting") == 3

    def test_completely_different(self):
        assert levenshtein_distance("abc", "xyz") == 3

    def test_symmetric(self):
        assert levenshtein_distance("abc", "def") == levenshtein_distance("def", "abc")


class TestDamerauLevenshteinDistance:
    def test_identical(self):
        assert damerau_levenshtein_distance("hello", "hello") == 0

    def test_transposition(self):
        assert damerau_levenshtein_distance("ab", "ba") == 1

    def test_insertion(self):
        assert damerau_levenshtein_distance("cat", "cats") == 1

    def test_classic(self):
        assert damerau_levenshtein_distance("ca", "abc") == 3


class TestJaroSimilarity:
    def test_identical(self):
        assert jaro_similarity("hello", "hello") == 1.0

    def test_empty(self):
        assert jaro_similarity("", "") == 1.0
        assert jaro_similarity("abc", "") == 0.0

    def test_no_match(self):
        assert jaro_similarity("abc", "xyz") == 0.0

    def test_partial_match(self):
        score = jaro_similarity("martha", "marhta")
        assert 0.9 < score < 1.0  # Transposed characters

    def test_range(self):
        score = jaro_similarity("hello", "world")
        assert 0.0 <= score <= 1.0


class TestJaroWinklerSimilarity:
    def test_identical(self):
        assert jaro_winkler_similarity("hello", "hello") == 1.0

    def test_prefix_bonus(self):
        jaro = jaro_similarity("hello", "help")
        jw = jaro_winkler_similarity("hello", "help")
        assert jw >= jaro  # Winkler should be >= Jaro

    def test_empty(self):
        assert jaro_winkler_similarity("", "") == 1.0

    def test_range(self):
        score = jaro_winkler_similarity("hello", "world")
        assert 0.0 <= score <= 1.0


class TestCosineSimilarity:
    def test_identical(self):
        assert abs(cosine_similarity("hello", "hello") - 1.0) < 0.01

    def test_empty(self):
        assert cosine_similarity("", "") == 0.0

    def test_no_common_bigrams(self):
        assert cosine_similarity("ab", "cd") == 0.0

    def test_range(self):
        score = cosine_similarity("hello world", "hello there")
        assert 0.0 <= score <= 1.0


class TestJaccardSimilarity:
    def test_identical(self):
        assert abs(jaccard_similarity("hello", "hello") - 1.0) < 0.01

    def test_empty(self):
        assert jaccard_similarity("", "") == 0.0

    def test_no_overlap(self):
        assert jaccard_similarity("ab", "cd") == 0.0

    def test_partial_overlap(self):
        score = jaccard_similarity("hello", "hallo")
        assert 0.0 < score < 1.0


class TestSorensenDice:
    def test_identical(self):
        assert abs(sorensen_dice_coefficient("hello", "hello") - 1.0) < 0.01

    def test_empty(self):
        assert sorensen_dice_coefficient("", "") == 0.0

    def test_no_overlap(self):
        assert sorensen_dice_coefficient("ab", "cd") == 0.0

    def test_partial(self):
        score = sorensen_dice_coefficient("night", "nacht")
        assert 0.0 < score < 1.0


class TestHammingDistance:
    def test_identical(self):
        assert hamming_distance("abc", "abc") == 0

    def test_all_different(self):
        assert hamming_distance("abc", "xyz") == 3

    def test_one_different(self):
        assert hamming_distance("abc", "axc") == 1

    def test_different_lengths_raises(self):
        with pytest.raises(ValueError):
            hamming_distance("abc", "ab")


class TestNormalizedLevenshtein:
    def test_identical(self):
        assert normalized_levenshtein("abc", "abc") == 0.0

    def test_empty(self):
        assert normalized_levenshtein("", "") == 0.0

    def test_completely_different(self):
        assert normalized_levenshtein("abc", "xyz") == 1.0

    def test_range(self):
        score = normalized_levenshtein("hello", "world")
        assert 0.0 <= score <= 1.0
