# Workato SDK Documentation Mirror - Testing

## Overview

Test suite for the Workato SDK Documentation Mirror, which fetches and converts Workato SDK documentation to Markdown.

## Test Files

```
tests/
├── test_basic_setup.py       # Environment and dependency validation
├── test_change_detection.py  # Content hashing and manifest tracking
├── test_integration_fetch.py # End-to-end documentation fetching
├── test_performance.py       # Performance benchmarks
└── test_unit_core.py         # Core parsing and conversion logic
```

### test_unit_core.py
Unit tests for `WorkatoDocsConverter` class:
- URL parsing and filename generation
- HTML content extraction
- Markdown conversion
- Manifest management

### test_integration_fetch.py
Integration tests for the full fetching pipeline:
- End-to-end documentation retrieval
- Network error handling
- Rate limiting behavior

### test_change_detection.py
Tests for content change tracking:
- SHA-256 content hashing
- Manifest file operations
- Skip logic for unchanged content

### test_basic_setup.py
Environment validation:
- Python version compatibility
- Dependency availability
- Project structure verification

### test_performance.py
Performance benchmarks:
- Memory usage with large HTML
- Processing time for batch operations
- Timeout handling

## Running Tests

```bash
# Run all tests
make test

# Quick validation during development
make test-fast

# Run with coverage report
make coverage

# Run specific test file
uv run pytest tests/test_unit_core.py

# Run with verbose output
uv run pytest tests/ -v
```

## Testing Tools

- **pytest**: Test framework
- **pytest-cov**: Coverage reporting
- **pytest-mock**: Mocking utilities
- **pytest-timeout**: Timeout handling
- **responses** / **requests-mock**: HTTP mocking
- **freezegun**: Time manipulation

## Coverage

- Target: 80% minimum (enforced by Codecov)
- Coverage reports uploaded to Codecov on CI
- Run `make coverage` locally to generate HTML report
