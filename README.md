# TextForge 🔨

**Universal text processing toolkit** — similarity, statistics, extraction, validation, transformation, comparison, and chunking.

TextForge is a comprehensive CLI tool and Python library for working with text. It provides algorithms for string comparison, text analysis, pattern extraction, format validation, case conversion, text diffing, and intelligent chunking — all in one place.

## Quick Start

```bash
# Install
pip install textforge

# Compare two strings
textforge sim compare "hello" "world"

# Analyze text statistics
textforge stats analyze "The quick brown fox jumps over the lazy dog."

# Extract patterns from text
textforge extract all "Email user@example.com and visit https://example.com"

# Validate formats
textforge validate email "user@example.com"
textforge validate uuid "550e8400-e29b-41d4-a716-446655440000"

# Transform text
textforge transform case "camelCase" --to snake
textforge transform case "hello world" --to kebab

# Compare texts
textforge compare diff "hello world" "hello earth"

# Chunk text for RAG
textforge chunk overlap "Long text here..." --chunk-size 500 --overlap 50
```

## Features

### 🔗 String Similarity (`textforge sim`)
Compare strings using multiple algorithms:
- **Levenshtein Distance** — classic edit distance (insert, delete, substitute)
- **Damerau-Levenshtein** — includes adjacent transpositions
- **Jaro / Jaro-Winkler** — prefix-weighted similarity
- **Cosine Similarity** — character bigram frequency vectors
- **Jaccard Similarity** — bigram set intersection/union
- **Sørensen-Dice** — weighted bigram overlap
- **Hamming Distance** — positional character differences

### 📊 Text Statistics (`textforge stats`)
Analyze text properties:
- Word, sentence, and paragraph counts
- Shannon entropy (randomness measure)
- Readability scores (Flesch Reading Ease, Flesch-Kincaid Grade)
- Type-Token Ratio (lexical diversity)
- Character density (letters, digits, spaces, punctuation)
- Lexical density (content vs function words)

### 🔍 Pattern Extraction (`textforge extract`)
Extract structured data from unstructured text:
- Email addresses
- URLs (http, https, www)
- Phone numbers (international formats)
- IPv4 and IPv6 addresses
- UUIDs (v1-v5)
- Dates (ISO, US, written formats)
- Hex color codes (#RGB, #RRGGBB)

### ✅ Format Validation (`textforge validate`)
Validate common formats:
- Email addresses
- URLs
- IP addresses (IPv4/IPv6)
- UUIDs
- Hex colors
- Dates
- Semantic versions (semver)
- JSON

### 🔄 Text Transformation (`textforge transform`)
Convert and transform text:
- **Case conversion**: snake_case, camelCase, PascalCase, kebab-case, SCREAMING_SNAKE, dot.case, Title Case
- **Slug generation** with Unicode normalization
- **Whitespace normalization**
- **Text truncation** with word-boundary awareness
- **Text wrapping** to specified width

### ⚖️ Text Comparison (`textforge compare`)
Diff and compare texts:
- **Character-level diff** (LCS-based)
- **Word-level diff**
- **Line-level diff**
- **Line similarity** score
- **Unified diff** output

### ✂️ Text Chunking (`textforge chunk`)
Split text into manageable pieces:
- **By sentences** with max size constraint
- **By paragraphs**
- **By word count**
- **By character count** with word-boundary breaks
- **Overlapping chunks** for RAG pipelines

## Library API

```python
from textforge import (
    # Similarity
    levenshtein_distance, jaro_winkler_similarity, cosine_similarity,
    # Statistics
    shannon_entropy, readability_score, type_token_ratio,
    # Extraction
    extract_emails, extract_urls, extract_ip_addresses,
    # Validation
    is_valid_email, is_valid_uuid, is_valid_semver,
    # Transform
    to_snake_case, to_camel_case, to_slug,
    # Compare
    diff_lines, diff_words, line_similarity,
    # Chunking
    chunk_by_sentences, chunk_with_overlap,
)

# Similarity
levenshtein_distance("kitten", "sitting")  # 3
jaro_winkler_similarity("hello", "help")   # 0.94

# Statistics
shannon_entropy("hello world")  # ~3.18 bits/char
readability_score("Simple text.")  # {'flesch_ease': ..., 'flesch_kincaid_grade': ...}

# Extraction
extract_emails("Contact user@example.com")  # [Extraction('email', 'user@example.com', ...)]

# Validation
is_valid_semver("1.0.0-beta.1")  # True

# Transform
to_snake_case("camelCase")  # 'camel_case'
to_slug("Hello, World!")    # 'hello-world'

# Compare
diff_words("hello world", "hello earth")  # [DiffItem(EQUAL, 'hello'), DiffItem(DELETE, 'world'), ...]

# Chunking
chunk_with_overlap("long text...", chunk_size=500, overlap=50)
```

## Architecture

```
textforge/
├── textforge/
│   ├── __init__.py       # Public API exports
│   ├── similarity.py     # String similarity algorithms (Levenshtein, Jaro, Cosine, etc.)
│   ├── statistics.py     # Text analysis (entropy, readability, TTR, etc.)
│   ├── extraction.py     # Pattern extraction (emails, URLs, IPs, UUIDs, etc.)
│   ├── validation.py     # Format validation (email, URL, UUID, semver, etc.)
│   ├── transform.py      # Text transformation (case, slug, wrap, truncate)
│   ├── compare.py        # Text comparison and diffing (LCS-based)
│   ├── chunking.py       # Text chunking (sentences, words, overlap)
│   └── cli.py            # CLI interface (Click + Rich)
├── tests/
│   ├── test_similarity.py
│   ├── test_statistics.py
│   ├── test_extraction.py
│   ├── test_validation.py
│   ├── test_transform.py
│   ├── test_compare.py
│   ├── test_chunking.py
│   └── test_cli.py
├── pyproject.toml
├── README.md
├── LICENSE
├── AGENTS.md
└── SECURITY.md
```

## Algorithms

| Module | Algorithm | Complexity |
|--------|-----------|------------|
| Similarity | Levenshtein Distance | O(m×n) time, O(min(m,n)) space |
| Similarity | Damerau-Levenshtein | O(m×n) time, O(m×n) space |
| Similarity | Jaro Similarity | O(m×n) time, O(m+n) space |
| Similarity | Cosine Similarity | O(m+n) time, O(m+n) space |
| Statistics | Shannon Entropy | O(n) time, O(k) space (k = unique chars) |
| Statistics | Flesch-Kincaid | O(n) time |
| Compare | LCS Diff | O(m×n) time, O(m×n) space |
| Chunking | Overlap Chunking | O(n) time, O(n) space |

## License

MIT
