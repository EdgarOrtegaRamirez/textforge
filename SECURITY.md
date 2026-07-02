# Security

TextForge is a text processing toolkit that operates locally on text data.

## No Network Requests

TextForge does not make any network requests. All processing happens locally.

## No Secrets Handling

TextForge does not handle, store, or transmit secrets, API keys, or credentials.

## Input Validation

- All CLI inputs are validated before processing
- Pattern extraction uses compiled regex patterns to prevent ReDoS
- No dynamic code execution (no `eval()`, `exec()`, or `subprocess`)

## Dependencies

TextForge has minimal dependencies:
- `click` — CLI framework (well-maintained, widely used)
- `rich` — Terminal formatting (well-maintained, widely used)

No dependencies with known vulnerabilities.

## Reporting Issues

If you discover a security issue, please report it responsibly by opening an issue on GitHub.
