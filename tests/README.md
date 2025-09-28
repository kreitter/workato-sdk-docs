# Workato SDK Documentation Mirror - Testing Strategy

## Overview
This test suite ensures the reliability and correctness of the Workato SDK Documentation Mirror project, which scrapes, converts, and maintains offline documentation from Workato's website.

## Test Categories

### 1. Unit Tests (`test_*.py`)
Test individual functions and methods in isolation.

**Core Components to Test:**
- `fetch_workato_docs.py`: URL parsing, HTML extraction, markdown conversion, manifest management
- `installer.py`: Installation logic, Claude integration, Git operations
- Helper utilities: URL validation, filename generation, content hashing

### 2. Integration Tests (`test_integration_*.py`)
Test interactions between components.

**Key Integration Points:**
- End-to-end documentation fetching pipeline
- GitHub Actions workflow execution
- Claude Code command integration
- Installation process

### 3. Regression Tests (`test_regression_*.py`)
Test against known good outputs and edge cases.

**Regression Test Areas:**
- HTML parsing with various Workato page structures
- Content validation against known good samples
- Error handling with network failures
- Git operations with various repository states

### 4. Performance Tests (`test_performance.py`)
Test efficiency and resource usage.

**Performance Concerns:**
- Memory usage with large HTML pages
- Network timeout handling
- Batch processing efficiency
- Git operation performance

## Test Data Strategy

### Mock Data
- Sample HTML from various Workato page types
- Mock network responses
- Test fixtures for different error conditions

### Real Data (Limited)
- Use actual URLs for integration tests
- Validate against real Workato documentation structure
- Test with live data in CI environment

## Test Execution

### Local Development
```bash
# Run all tests
uv run pytest tests/

# Run specific test categories
uv run pytest tests/test_unit_*.py
uv run pytest tests/test_integration_*.py

# Run with coverage
uv run pytest --cov=workato_sdk_docs tests/

# Run performance tests
uv run pytest tests/test_performance.py --durations=10
```

### CI/CD Integration
- Run full test suite on every PR
- Performance tests on main branch
- Integration tests with real network calls
- Regression tests against live Workato docs

## Test Coverage Goals

### Code Coverage
- **Target**: >85% code coverage
- **Critical**: 100% coverage for error handling paths
- **Core Functions**: 100% coverage for URL parsing, HTML extraction, markdown conversion

### Scenario Coverage
- All documented error conditions
- Various HTML structure formats
- Different repository states
- Network failure scenarios
- File system error conditions

## Testing Tools

### Primary Framework
- **pytest**: Main testing framework
- **pytest-cov**: Code coverage reporting
- **pytest-mock**: Mocking utilities
- **pytest-timeout**: Timeout handling for slow tests

### Additional Tools
- **responses**: Mock HTTP responses
- **requests-mock**: Network request mocking
- **freezegun**: Time manipulation for tests
- **tmp_path**: Temporary file handling

## Test Organization

```
tests/
├── __init__.py
├── README.md
├── fixtures/
│   ├── sample_html/
│   ├── mock_responses/
│   └── test_data/
├── test_unit_core.py          # Core parsing and conversion
├── test_unit_installer.py     # Installation logic
├── test_unit_utils.py         # Utility functions
├── test_integration_fetch.py  # End-to-end fetching
├── test_integration_install.py # Installation process
├── test_integration_claude.py # Claude Code integration
├── test_regression_parsing.py # HTML parsing regression
├── test_regression_content.py  # Content validation
└── test_performance.py        # Performance benchmarks
```

## Critical Test Scenarios

### 1. HTML Parsing Robustness
- Test with malformed HTML
- Test with missing expected elements
- Test with different page structures
- Test with JavaScript-heavy pages

### 2. Network Resilience
- Test with network timeouts
- Test with HTTP errors (404, 500, etc.)
- Test with rate limiting
- Test with slow connections

### 3. File System Operations
- Test with permission errors
- Test with disk full scenarios
- Test with invalid paths
- Test with concurrent access

### 4. Git Operations
- Test with dirty working directory
- Test with network Git failures
- Test with authentication issues
- Test with branch conflicts

### 5. Content Validation
- Test with empty content
- Test with binary content
- Test with extremely large content
- Test with special characters/encoding

## Maintenance

### Regular Updates
- Update test fixtures when Workato changes HTML structure
- Add tests for new features
- Remove obsolete tests
- Update performance benchmarks

### CI/CD Monitoring
- Track test execution time trends
- Monitor flaky test rates
- Alert on coverage decreases
- Track error patterns in test failures
