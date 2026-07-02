"""Tests for textforge CLI."""

import json

import pytest
from click.testing import CliRunner

from textforge.cli import main


@pytest.fixture
def runner():
    return CliRunner()


class TestCLI:
    def test_version(self, runner):
        result = runner.invoke(main, ["--version"])
        assert result.exit_code == 0
        assert "textforge" in result.output.lower() or "0.1.0" in result.output

    def test_sim_compare(self, runner):
        result = runner.invoke(main, ["sim", "compare", "hello", "world"])
        assert result.exit_code == 0
        assert "Levenshtein" in result.output

    def test_sim_compare_single_metric(self, runner):
        result = runner.invoke(main, ["sim", "compare", "hello", "world", "-m", "cosine"])
        assert result.exit_code == 0

    def test_stats_analyze(self, runner):
        result = runner.invoke(main, ["stats", "analyze", "Hello world. This is a test."])
        assert result.exit_code == 0
        assert "Words" in result.output

    def test_stats_analyze_json(self, runner):
        result = runner.invoke(main, ["stats", "analyze", "Hello world.", "-j"])
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert "word_count" in data

    def test_extract_all(self, runner):
        result = runner.invoke(main, ["extract", "all", "Email user@example.com and visit https://example.com"])
        assert result.exit_code == 0
        assert "email" in result.output.lower() or "user@example.com" in result.output

    def test_extract_emails(self, runner):
        result = runner.invoke(main, ["extract", "emails", "Contact user@example.com"])
        assert result.exit_code == 0
        assert "user@example.com" in result.output

    def test_validate_email_valid(self, runner):
        result = runner.invoke(main, ["validate", "email", "user@example.com"])
        assert result.exit_code == 0
        assert "valid" in result.output.lower()

    def test_validate_email_invalid(self, runner):
        result = runner.invoke(main, ["validate", "email", "notanemail"])
        assert result.exit_code == 1

    def test_validate_url(self, runner):
        result = runner.invoke(main, ["validate", "url", "https://example.com"])
        assert result.exit_code == 0

    def test_validate_uuid(self, runner):
        result = runner.invoke(main, ["validate", "uuid", "550e8400-e29b-41d4-a716-446655440000"])
        assert result.exit_code == 0

    def test_transform_case_snake(self, runner):
        result = runner.invoke(main, ["transform", "case", "camelCase", "--to", "snake"])
        assert result.exit_code == 0
        assert "camel_case" in result.output

    def test_transform_case_kebab(self, runner):
        result = runner.invoke(main, ["transform", "case", "PascalCase", "--to", "kebab"])
        assert result.exit_code == 0
        assert "pascal-case" in result.output

    def test_transform_truncate(self, runner):
        result = runner.invoke(main, ["transform", "truncate", "hello world foo", "--max-length", "8"])
        assert result.exit_code == 0
        assert len(result.output.strip()) <= 8

    def test_compare_diff(self, runner):
        result = runner.invoke(main, ["compare", "diff", "hello", "world"])
        assert result.exit_code == 0

    def test_compare_similarity(self, runner):
        result = runner.invoke(main, ["compare", "similarity", "hello\nworld", "hello\nthere"])
        assert result.exit_code == 0
        assert "similarity" in result.output.lower()

    def test_chunk_sentences(self, runner):
        result = runner.invoke(main, ["chunk", "sentences", "First. Second. Third."])
        assert result.exit_code == 0
        assert "Chunk" in result.output

    def test_chunk_words(self, runner):
        result = runner.invoke(main, ["chunk", "words", "one two three four five", "-w", "2"])
        assert result.exit_code == 0
