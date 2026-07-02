"""Tests for textforge.transform module."""

from textforge.transform import (
    dedent_text,
    normalize_whitespace,
    title_case,
    to_camel_case,
    to_dot_case,
    to_kebab_case,
    to_pascal_case,
    to_screaming_snake,
    to_slug,
    to_snake_case,
    truncate_text,
    wrap_text,
)


class TestToSnakeCase:
    def test_camel(self):
        assert to_snake_case("camelCase") == "camel_case"

    def test_pascal(self):
        assert to_snake_case("PascalCase") == "pascal_case"

    def test_kebab(self):
        assert to_snake_case("kebab-case") == "kebab_case"

    def test_spaces(self):
        assert to_snake_case("Hello World") == "hello_world"

    def test_already_snake(self):
        assert to_snake_case("already_snake") == "already_snake"

    def test_empty(self):
        assert to_snake_case("") == ""

    def test_single_word(self):
        assert to_snake_case("hello") == "hello"


class TestToCamelCase:
    def test_snake(self):
        assert to_camel_case("snake_case") == "snakeCase"

    def test_kebab(self):
        assert to_camel_case("kebab-case") == "kebabCase"

    def test_spaces(self):
        assert to_camel_case("Hello World") == "helloWorld"

    def test_pascal(self):
        assert to_camel_case("PascalCase") == "pascalCase"


class TestToPascalCase:
    def test_snake(self):
        assert to_pascal_case("snake_case") == "SnakeCase"

    def test_kebab(self):
        assert to_pascal_case("kebab-case") == "KebabCase"

    def test_spaces(self):
        assert to_pascal_case("Hello World") == "HelloWorld"


class TestToKebabCase:
    def test_camel(self):
        assert to_kebab_case("camelCase") == "camel-case"

    def test_pascal(self):
        assert to_kebab_case("PascalCase") == "pascal-case"

    def test_snake(self):
        assert to_kebab_case("snake_case") == "snake-case"


class TestToScreamingSnake:
    def test_camel(self):
        assert to_screaming_snake("camelCase") == "CAMEL_CASE"

    def test_kebab(self):
        assert to_screaming_snake("kebab-case") == "KEBAB_CASE"


class TestToDotCase:
    def test_camel(self):
        assert to_dot_case("camelCase") == "camel.case"

    def test_snake(self):
        assert to_dot_case("snake_case") == "snake.case"


class TestToSlug:
    def test_basic(self):
        assert to_slug("Hello, World!") == "hello-world"

    def test_unicode(self):
        assert to_slug("Café Résumé") == "cafe-resume"

    def test_custom_separator(self):
        assert to_slug("Hello World", separator="_") == "hello_world"

    def test_multiple_spaces(self):
        assert to_slug("hello   world") == "hello-world"


class TestNormalizeWhitespace:
    def test_multiple_spaces(self):
        assert normalize_whitespace("hello  world") == "hello world"

    def test_tabs(self):
        assert normalize_whitespace("hello\tworld") == "hello world"

    def test_leading_trailing(self):
        assert normalize_whitespace("  hello  ") == "hello"

    def test_multiline(self):
        result = normalize_whitespace("  hello\n  world  ")
        assert result == "hello\nworld"


class TestTruncateText:
    def test_no_truncation(self):
        assert truncate_text("hello", 10) == "hello"

    def test_truncation(self):
        result = truncate_text("hello world foo bar", 10)
        assert len(result) <= 10
        assert result.endswith("...")

    def test_custom_suffix(self):
        result = truncate_text("hello world", 8, suffix="~")
        assert result.endswith("~")

    def test_exact_length(self):
        assert truncate_text("hello", 5) == "hello"


class TestWrapText:
    def test_basic(self):
        result = wrap_text("hello world foo bar", width=10)
        lines = result.split("\n")
        for line in lines:
            assert len(line) <= 10

    def test_indent(self):
        result = wrap_text("hello world", width=50, indent="  ")
        assert result.startswith("  ")

    def test_single_word(self):
        result = wrap_text("hello", width=10)
        assert result == "hello"


class TestDedentText:
    def test_basic(self):
        text = "    hello\n    world"
        result = dedent_text(text)
        assert result == "hello\nworld"


class TestTitleCase:
    def test_basic(self):
        assert title_case("the quick brown fox") == "The Quick Brown Fox"

    def test_small_words(self):
        assert title_case("a tale of two cities") == "A Tale of Two Cities"

    def test_first_word_not_lowered(self):
        assert title_case("the answer") == "The Answer"
