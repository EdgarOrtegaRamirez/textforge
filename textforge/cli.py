"""TextForge CLI — universal text processing toolkit."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import click
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()


@click.group()
@click.version_option(package_name="textforge")
def main() -> None:
    """TextForge — Universal text processing toolkit.

    Similarity, statistics, extraction, validation, transformation,
    comparison, and chunking of text.
    """


# ── Similarity ──────────────────────────────────────────────────────────────


@main.group()
def sim() -> None:
    """String similarity algorithms."""


@sim.command("compare")
@click.argument("s1")
@click.argument("s2")
@click.option(
    "--metric",
    "-m",
    type=click.Choice(
        [
            "levenshtein",
            "damerau",
            "jaro",
            "jaro-winkler",
            "cosine",
            "jaccard",
            "dice",
            "hamming",
            "all",
        ]
    ),
    default="all",
    help="Similarity metric to use.",
)
def sim_compare(s1: str, s2: str, metric: str) -> None:
    """Compare two strings using similarity metrics."""
    from textforge.similarity import (
        cosine_similarity,
        damerau_levenshtein_distance,
        hamming_distance,
        jaccard_similarity,
        jaro_similarity,
        jaro_winkler_similarity,
        levenshtein_distance,
        sorensen_dice_coefficient,
    )

    table = Table(title=f"Similarity: {s1!r} vs {s2!r}")
    table.add_column("Metric", style="cyan")
    table.add_column("Value", style="green")

    metrics = {
        "levenshtein": ("Levenshtein Distance", levenshtein_distance(s1, s2)),
        "damerau": ("Damerau-Levenshtein", damerau_levenshtein_distance(s1, s2)),
        "jaro": ("Jaro Similarity", jaro_similarity(s1, s2)),
        "jaro-winkler": ("Jaro-Winkler", jaro_winkler_similarity(s1, s2)),
        "cosine": ("Cosine Similarity", cosine_similarity(s1, s2)),
        "jaccard": ("Jaccard Similarity", jaccard_similarity(s1, s2)),
        "dice": ("Sørensen-Dice", sorensen_dice_coefficient(s1, s2)),
        "hamming": ("Hamming Distance", hamming_distance(s1, s2) if len(s1) == len(s2) else "N/A (different lengths)"),
    }

    if metric == "all":
        for _name, (label, value) in metrics.items():
            if isinstance(value, float):
                table.add_row(label, f"{value:.4f}")
            else:
                table.add_row(label, str(value))
    else:
        label, value = metrics[metric]
        if isinstance(value, float):
            table.add_row(label, f"{value:.4f}")
        else:
            table.add_row(label, str(value))

    console.print(table)


# ── Statistics ──────────────────────────────────────────────────────────────


@main.group()
def stats() -> None:
    """Text statistics and analysis."""


@stats.command("analyze")
@click.argument("text", required=False)
@click.option("--file", "-f", type=click.Path(exists=True), help="Read text from file.")
@click.option("--json-output", "-j", is_flag=True, help="Output as JSON.")
def stats_analyze(text: str | None, file: str | None, json_output: bool) -> None:
    """Analyze text statistics (word count, entropy, readability, etc.)."""
    from textforge.statistics import (
        average_word_length,
        character_density,
        paragraph_count,
        readability_score,
        sentence_count,
        shannon_entropy,
        type_token_ratio,
        word_count,
    )

    if file:
        content = Path(file).read_text()
    elif text:
        content = text
    elif not sys.stdin.isatty():
        content = sys.stdin.read()
    else:
        console.print("[red]Error:[/red] Provide text as argument, --file, or via stdin.")
        sys.exit(1)

    result = {
        "word_count": word_count(content),
        "sentence_count": sentence_count(content),
        "paragraph_count": paragraph_count(content),
        "character_count": len(content),
        "shannon_entropy": round(shannon_entropy(content), 4),
        "average_word_length": round(average_word_length(content), 2),
        "type_token_ratio": round(type_token_ratio(content), 4),
        "readability": readability_score(content),
        "character_density": {k: round(v, 4) for k, v in character_density(content).items()},
    }

    if json_output:
        click.echo(json.dumps(result, indent=2))
    else:
        table = Table(title="Text Statistics")
        table.add_column("Metric", style="cyan")
        table.add_column("Value", style="green")
        table.add_row("Words", str(result["word_count"]))
        table.add_row("Sentences", str(result["sentence_count"]))
        table.add_row("Paragraphs", str(result["paragraph_count"]))
        table.add_row("Characters", str(result["character_count"]))
        table.add_row("Shannon Entropy", f"{result['shannon_entropy']:.4f} bits/char")
        table.add_row("Avg Word Length", f"{result['average_word_length']:.2f}")
        table.add_row("Type-Token Ratio", f"{result['type_token_ratio']:.4f}")
        table.add_row("Flesch Reading Ease", f"{result['readability']['flesch_ease']:.1f}")
        table.add_row("Flesch-Kincaid Grade", f"{result['readability']['flesch_kincaid_grade']:.1f}")
        console.print(table)


# ── Extraction ──────────────────────────────────────────────────────────────


@main.group()
def extract() -> None:
    """Extract patterns from text."""


@extract.command("all")
@click.argument("text", required=False)
@click.option("--file", "-f", type=click.Path(exists=True), help="Read text from file.")
@click.option("--json-output", "-j", is_flag=True, help="Output as JSON.")
def extract_all(text: str | None, file: str | None, json_output: bool) -> None:
    """Extract all recognized patterns (emails, URLs, IPs, etc.)."""
    from textforge.extraction import extract_all as do_extract_all

    if file:
        content = Path(file).read_text()
    elif text:
        content = text
    elif not sys.stdin.isatty():
        content = sys.stdin.read()
    else:
        console.print("[red]Error:[/red] Provide text as argument, --file, or via stdin.")
        sys.exit(1)

    results = do_extract_all(content)

    if json_output:
        data = [{"pattern": r.pattern, "value": r.value, "start": r.start, "end": r.end} for r in results]
        click.echo(json.dumps(data, indent=2))
    else:
        if not results:
            console.print("[yellow]No patterns found.[/yellow]")
            return
        table = Table(title="Extracted Patterns")
        table.add_column("Pattern", style="cyan")
        table.add_column("Value", style="green")
        table.add_column("Position", style="dim")
        for r in results:
            table.add_row(r.pattern, r.value, f"{r.start}-{r.end}")
        console.print(table)


@extract.command("emails")
@click.argument("text", required=False)
@click.option("--file", "-f", type=click.Path(exists=True))
def extract_emails_cmd(text: str | None, file: str | None) -> None:
    """Extract email addresses."""
    from textforge.extraction import extract_emails

    _extract_pattern(text, file, extract_emails, "emails")


@extract.command("urls")
@click.argument("text", required=False)
@click.option("--file", "-f", type=click.Path(exists=True))
def extract_urls_cmd(text: str | None, file: str | None) -> None:
    """Extract URLs."""
    from textforge.extraction import extract_urls

    _extract_pattern(text, file, extract_urls, "urls")


@extract.command("ips")
@click.argument("text", required=False)
@click.option("--file", "-f", type=click.Path(exists=True))
def extract_ips_cmd(text: str | None, file: str | None) -> None:
    """Extract IP addresses."""
    from textforge.extraction import extract_ip_addresses

    _extract_pattern(text, file, extract_ip_addresses, "IP addresses")


# ── Validation ──────────────────────────────────────────────────────────────


@main.group()
def validate() -> None:
    """Validate text formats."""


@validate.command("email")
@click.argument("value")
def validate_email(value: str) -> None:
    """Validate an email address."""
    from textforge.validation import is_valid_email

    _validate(is_valid_email(value), value, "email")


@validate.command("url")
@click.argument("value")
def validate_url(value: str) -> None:
    """Validate a URL."""
    from textforge.validation import is_valid_url

    _validate(is_valid_url(value), value, "URL")


@validate.command("ip")
@click.argument("value")
def validate_ip(value: str) -> None:
    """Validate an IP address."""
    from textforge.validation import is_valid_ip_address

    _validate(is_valid_ip_address(value), value, "IP address")


@validate.command("uuid")
@click.argument("value")
def validate_uuid(value: str) -> None:
    """Validate a UUID."""
    from textforge.validation import is_valid_uuid

    _validate(is_valid_uuid(value), value, "UUID")


@validate.command("color")
@click.argument("value")
def validate_color(value: str) -> None:
    """Validate a hex color code."""
    from textforge.validation import is_valid_hex_color

    _validate(is_valid_hex_color(value), value, "hex color")


@validate.command("date")
@click.argument("value")
def validate_date(value: str) -> None:
    """Validate a date string."""
    from textforge.validation import is_valid_date

    _validate(is_valid_date(value), value, "date")


@validate.command("semver")
@click.argument("value")
def validate_semver(value: str) -> None:
    """Validate a semantic version string."""
    from textforge.validation import is_valid_semver

    _validate(is_valid_semver(value), value, "semver")


# ── Transform ───────────────────────────────────────────────────────────────


@main.group()
def transform() -> None:
    """Text transformation functions."""


@transform.command("case")
@click.argument("text")
@click.option(
    "--to",
    "-t",
    type=click.Choice(
        [
            "snake",
            "camel",
            "pascal",
            "kebab",
            "screaming",
            "dot",
            "slug",
            "title",
        ]
    ),
    required=True,
    help="Target case format.",
)
def transform_case(text: str, to: str) -> None:
    """Convert text to a different case format."""
    from textforge.transform import (
        title_case,
        to_camel_case,
        to_dot_case,
        to_kebab_case,
        to_pascal_case,
        to_screaming_snake,
        to_slug,
        to_snake_case,
    )

    converters = {
        "snake": to_snake_case,
        "camel": to_camel_case,
        "pascal": to_pascal_case,
        "kebab": to_kebab_case,
        "screaming": to_screaming_snake,
        "dot": to_dot_case,
        "slug": to_slug,
        "title": title_case,
    }

    result = converters[to](text)
    click.echo(result)


@transform.command("truncate")
@click.argument("text")
@click.option("--max-length", "-l", type=int, required=True, help="Maximum length.")
@click.option("--suffix", "-s", default="...", help="Suffix when truncated.")
def transform_truncate(text: str, max_length: int, suffix: str) -> None:
    """Truncate text to a maximum length."""
    from textforge.transform import truncate_text

    click.echo(truncate_text(text, max_length, suffix))


@transform.command("wrap")
@click.argument("text", required=False)
@click.option("--file", "-f", type=click.Path(exists=True))
@click.option("--width", "-w", type=int, default=80, help="Line width.")
def transform_wrap(text: str | None, file: str | None, width: int) -> None:
    """Wrap text to a specified width."""
    from textforge.transform import wrap_text

    if file:
        content = Path(file).read_text()
    elif text:
        content = text
    elif not sys.stdin.isatty():
        content = sys.stdin.read()
    else:
        console.print("[red]Error:[/red] Provide text as argument, --file, or via stdin.")
        sys.exit(1)

    click.echo(wrap_text(content, width))


@transform.command("normalize")
@click.argument("text", required=False)
@click.option("--file", "-f", type=click.Path(exists=True))
def transform_normalize(text: str | None, file: str | None) -> None:
    """Normalize whitespace in text."""
    from textforge.transform import normalize_whitespace

    if file:
        content = Path(file).read_text()
    elif text:
        content = text
    elif not sys.stdin.isatty():
        content = sys.stdin.read()
    else:
        console.print("[red]Error:[/red] Provide text as argument, --file, or via stdin.")
        sys.exit(1)

    click.echo(normalize_whitespace(content))


# ── Compare ─────────────────────────────────────────────────────────────────


@main.group()
def compare() -> None:
    """Text comparison and diffing."""


@compare.command("diff")
@click.argument("text1", required=False)
@click.argument("text2", required=False)
@click.option("--file1", "-1", type=click.Path(exists=True), help="First file.")
@click.option("--file2", "-2", type=click.Path(exists=True), help="Second file.")
@click.option(
    "--level",
    "-l",
    type=click.Choice(["chars", "words", "lines"]),
    default="lines",
    help="Diff granularity.",
)
@click.option("--json-output", "-j", is_flag=True, help="Output as JSON.")
def compare_diff(
    text1: str | None,
    text2: str | None,
    file1: str | None,
    file2: str | None,
    level: str,
    json_output: bool,
) -> None:
    """Compute diff between two texts."""
    from textforge.compare import DiffOp, diff_chars, diff_lines, diff_words

    s1 = _read_input(text1, file1, 1)
    s2 = _read_input(text2, file2, 2)

    diff_fn = {"chars": diff_chars, "words": diff_words, "lines": diff_lines}[level]
    result = diff_fn(s1, s2)

    if json_output:
        data = [{"op": d.op.value, "value": d.value} for d in result]
        click.echo(json.dumps(data, indent=2))
    else:
        for item in result:
            if item.op == DiffOp.EQUAL:
                click.echo(f"  {item.value}", err=False)
            elif item.op == DiffOp.INSERT:
                click.echo(f"+ {item.value}", err=False)
            elif item.op == DiffOp.DELETE:
                click.echo(f"- {item.value}", err=False)
            elif item.op == DiffOp.REPLACE:
                click.echo(f"~ {item.value}", err=False)


@compare.command("similarity")
@click.argument("text1", required=False)
@click.argument("text2", required=False)
@click.option("--file1", "-1", type=click.Path(exists=True))
@click.option("--file2", "-2", type=click.Path(exists=True))
def compare_similarity(text1: str | None, text2: str | None, file1: str | None, file2: str | None) -> None:
    """Compute line-level similarity between two texts."""
    from textforge.compare import line_similarity

    s1 = _read_input(text1, file1, 1)
    s2 = _read_input(text2, file2, 2)

    score = line_similarity(s1, s2)
    console.print(f"Line similarity: [green]{score:.4f}[/green] ({score * 100:.1f}%)")


# ── Chunk ───────────────────────────────────────────────────────────────────


@main.group()
def chunk() -> None:
    """Text chunking algorithms."""


@chunk.command("sentences")
@click.argument("text", required=False)
@click.option("--file", "-f", type=click.Path(exists=True))
@click.option("--max-size", "-s", type=int, default=500, help="Max chunk size in characters.")
@click.option("--json-output", "-j", is_flag=True, help="Output as JSON.")
def chunk_sentences(text: str | None, file: str | None, max_size: int, json_output: bool) -> None:
    """Chunk text by sentences."""
    from textforge.chunking import chunk_by_sentences

    content = _read_input(text, file, 0)
    chunks = chunk_by_sentences(content, max_size)
    _output_chunks(chunks, json_output)


@chunk.command("words")
@click.argument("text", required=False)
@click.option("--file", "-f", type=click.Path(exists=True))
@click.option("--words-per-chunk", "-w", type=int, default=100, help="Words per chunk.")
@click.option("--json-output", "-j", is_flag=True, help="Output as JSON.")
def chunk_words(text: str | None, file: str | None, words_per_chunk: int, json_output: bool) -> None:
    """Chunk text by word count."""
    from textforge.chunking import chunk_by_words

    content = _read_input(text, file, 0)
    chunks = chunk_by_words(content, words_per_chunk)
    _output_chunks(chunks, json_output)


@chunk.command("overlap")
@click.argument("text", required=False)
@click.option("--file", "-f", type=click.Path(exists=True))
@click.option("--chunk-size", "-s", type=int, default=500, help="Chunk size.")
@click.option("--overlap", "-o", type=int, default=50, help="Overlap size.")
@click.option("--by", "-b", type=click.Choice(["words", "chars"]), default="words")
@click.option("--json-output", "-j", is_flag=True, help="Output as JSON.")
def chunk_overlap(
    text: str | None,
    file: str | None,
    chunk_size: int,
    overlap: int,
    by: str,
    json_output: bool,
) -> None:
    """Chunk text with overlap (for RAG pipelines)."""
    from textforge.chunking import chunk_with_overlap

    content = _read_input(text, file, 0)
    chunks = chunk_with_overlap(content, chunk_size, overlap, by)
    _output_chunks(chunks, json_output)


# ── Helper functions ────────────────────────────────────────────────────────


def _read_input(text: str | None, file: str | None, arg_index: int) -> str:
    """Read input from argument, file, or stdin."""
    if file:
        return Path(file).read_text()
    if text:
        return text
    if not sys.stdin.isatty():
        return sys.stdin.read()
    console.print(f"[red]Error:[/red] Provide text as argument {arg_index}, --file, or via stdin.")
    sys.exit(1)


def _extract_pattern(text: str | None, file: str | None, func, label: str) -> None:
    """Helper for extraction commands."""
    content = _read_input(text, file, 0)
    results = func(content)
    if not results:
        console.print(f"[yellow]No {label} found.[/yellow]")
        return
    for r in results:
        click.echo(r.value)


def _validate(valid: bool, value: str, label: str) -> None:
    """Helper for validation commands."""
    if valid:
        console.print(f"[green]✓[/green] {value!r} is a valid {label}")
    else:
        console.print(f"[red]✗[/red] {value!r} is NOT a valid {label}")
        sys.exit(1)


def _output_chunks(chunks: list[str], json_output: bool) -> None:
    """Output chunks."""
    if json_output:
        click.echo(json.dumps(chunks, indent=2))
    else:
        for i, chunk_text in enumerate(chunks, 1):
            console.print(Panel(chunk_text, title=f"Chunk {i}", border_style="blue"))


if __name__ == "__main__":
    main()
