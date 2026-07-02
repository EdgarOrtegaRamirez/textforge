# AGENTS.md

## TextForge

Universal text processing toolkit — similarity, statistics, extraction, validation, transformation, comparison, and chunking.

### Building

```bash
uv sync --dev
```

### Testing

```bash
uv run pytest
```

### Linting

```bash
uv run ruff check .
uv run ruff format --check .
```

### Project Structure

- `textforge/` — Main package
  - `similarity.py` — String similarity algorithms (Levenshtein, Jaro, Cosine, etc.)
  - `statistics.py` — Text analysis (entropy, readability, TTR, etc.)
  - `extraction.py` — Pattern extraction (emails, URLs, IPs, UUIDs, etc.)
  - `validation.py` — Format validation (email, URL, UUID, semver, etc.)
  - `transform.py` — Text transformation (case, slug, wrap, truncate)
  - `compare.py` — Text comparison and diffing (LCS-based)
  - `chunking.py` — Text chunking (sentences, words, overlap)
  - `cli.py` — CLI interface (Click + Rich)
- `tests/` — Test suite (pytest)
- `pyproject.toml` — Project configuration

### Key Algorithms

- **Levenshtein Distance**: DP with O(min(m,n)) space optimization
- **Jaro-Winkler**: Prefix-weighted Jaro similarity
- **Cosine Similarity**: Character bigram frequency vectors
- **Shannon Entropy**: -Σ p(x) log₂ p(x)
- **LCS Diff**: Classic DP backtracking for optimal alignment
- **Overlap Chunking**: Sliding window with configurable overlap

### Dependencies

- `click` — CLI framework
- `rich` — Terminal formatting
- No heavy dependencies — all algorithms are pure Python
