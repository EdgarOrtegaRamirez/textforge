"""TextForge: Universal text processing toolkit."""

__version__ = "0.1.0"

from textforge.chunking import (
    chunk_by_characters,
    chunk_by_paragraphs,
    chunk_by_sentences,
    chunk_by_words,
    chunk_with_overlap,
)
from textforge.compare import (
    diff_chars,
    diff_lines,
    diff_words,
    line_similarity,
)
from textforge.extraction import (
    extract_dates,
    extract_emails,
    extract_hex_colors,
    extract_ip_addresses,
    extract_phone_numbers,
    extract_urls,
    extract_uuids,
)
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
from textforge.statistics import (
    average_sentence_length,
    average_word_length,
    character_frequency,
    paragraph_count,
    readability_score,
    sentence_count,
    shannon_entropy,
    word_count,
)
from textforge.transform import (
    dedent_text,
    normalize_whitespace,
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
from textforge.validation import (
    is_valid_date,
    is_valid_email,
    is_valid_hex_color,
    is_valid_ip_address,
    is_valid_isbn,
    is_valid_url,
    is_valid_uuid,
)

__all__ = [
    # Similarity
    "levenshtein_distance",
    "damerau_levenshtein_distance",
    "jaro_similarity",
    "jaro_winkler_similarity",
    "cosine_similarity",
    "jaccard_similarity",
    "sorensen_dice_coefficient",
    "hamming_distance",
    # Statistics
    "word_count",
    "sentence_count",
    "paragraph_count",
    "character_frequency",
    "shannon_entropy",
    "readability_score",
    "average_word_length",
    "average_sentence_length",
    # Extraction
    "extract_emails",
    "extract_urls",
    "extract_phone_numbers",
    "extract_ip_addresses",
    "extract_uuids",
    "extract_dates",
    "extract_hex_colors",
    # Validation
    "is_valid_email",
    "is_valid_url",
    "is_valid_ip_address",
    "is_valid_uuid",
    "is_valid_hex_color",
    "is_valid_date",
    "is_valid_isbn",
    # Transform
    "to_snake_case",
    "to_camel_case",
    "to_pascal_case",
    "to_kebab_case",
    "to_screaming_snake",
    "to_dot_case",
    "to_slug",
    "normalize_whitespace",
    "truncate_text",
    "wrap_text",
    "dedent_text",
    # Compare
    "diff_lines",
    "diff_words",
    "diff_chars",
    "line_similarity",
    # Chunking
    "chunk_by_sentences",
    "chunk_by_paragraphs",
    "chunk_by_words",
    "chunk_by_characters",
    "chunk_with_overlap",
]
