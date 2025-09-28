# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

Documentation mirror system that fetches Workato SDK HTML documentation and converts it to Markdown for local access in Claude Code. Provides `/workato-sdk` command integration for developers working with Workato Connector SDK.

## Essential Commands

### Development & Testing
```bash
# Run the documentation fetcher with uv (recommended - avoids system Python)
uv run python scripts/fetch_workato_docs.py

# Install and configure Claude Code integration
uvx --from git+https://github.com/kreitter/workato-sdk-docs.git workato-sdk-install

# Alternative: legacy installation (deprecated)
./install.sh

# Manual update of documentation cache
cd ~/.workato-sdk-docs && uv run python scripts/fetch_workato_docs.py

# Test single URL conversion
python3 -c "from scripts.fetch_workato_docs import WorkatoDocsConverter; WorkatoDocsConverter().convert_single('https://docs.workato.com/en/developing-connectors/sdk/cli.html')"
```

### GitHub Actions & CI/CD
```bash
# Trigger manual documentation update workflow
gh workflow run update-docs.yml

# View workflow execution history
gh run list --workflow=update-docs.yml

# Check workflow logs for debugging
gh run view <run-id> --log
```

### Development & Testing Commands
```bash
# Development workflow
make install-dev       # Install development dependencies
make setup-precommit   # Set up pre-commit hooks

# Testing (comprehensive test suite available)
make test             # Run all tests
make test-unit        # Unit tests only
make test-integration # Integration tests only
make test-regression  # Regression tests only
make test-performance # Performance tests only
make test-fast        # Fast tests (unit + regression)

# Code quality
make lint             # Run linting checks
make format           # Format code with black and isort
make coverage         # Run tests with coverage report

# Cleanup
make clean            # Remove temporary files and caches
```

### Testing Workflow
- **Pre-commit**: Tests run automatically before commits (fast unit tests)
- **CI/CD**: Full test suite runs on GitHub Actions for all PRs/pushes
- **Coverage**: Reports uploaded to Codecov with quality gates
- **43+ tests** covering unit, integration, regression, and error conditions
```

## Architecture

### Two Installation Methods

1. **Modern uv-based** (pyproject.toml): Isolated Python environment via `uvx`, avoids system Python conflicts
2. **Legacy bash-based** (install.sh): Direct system installation, deprecated due to PEP 668 restrictions

### Documentation Processing Pipeline

1. **Direct URL Fetching**: Hardcoded list of 90 SDK URLs in `scripts/fetch_workato_docs.py` (lines 36-127)
2. **HTML Extraction**: `WorkatoDocsConverter` class extracts content using BeautifulSoup selectors
3. **Markdown Conversion**: html2text converts with custom configuration
4. **Local Storage**: `docs/` directory with content hashing for change detection
5. **Claude Integration**: Shell script provides `/workato-sdk` command interface

### Key Components

```
workato_sdk_docs/               # Python package for uv installation
  installer.py                  # Modern installer logic
scripts/
  fetch_workato_docs.py         # Core fetcher (WorkatoDocsConverter class)
  workato-sdk-helper.sh.template # Command handler for Claude Code
.github/workflows/update-docs.yml # Daily GitHub Actions update (02:00 UTC)
docs/                           # Generated Markdown files (90 SDK docs)
docs_manifest.json              # Change tracking and metadata
```

## Critical Implementation Details

### HTML Content Extraction (`WorkatoDocsConverter.extract_main_content()`)
Update selectors when Workato changes their documentation HTML structure:

```python
selectors = [
    'main.content',
    'div.content',
    'article.doc-content',
    'div.doc-body',
    # Add new selectors if HTML structure changes
]
```

### URL Management
- `SDK_URLS` list (lines 36-127): 90 hardcoded SDK documentation URLs
- No crawling or discovery - explicit list prevents scope creep
- Excludes non-SDK pages (e.g., import-via-oas)
- Add new URLs directly to list when Workato adds documentation

### Fork Support
Installer automatically detects repository from:
1. Git remote (if in cloned repo): `git remote get-url origin`
2. Environment variable: `WORKATO_SDK_REPO_URL`
3. Command flag: `workato-sdk-install --repo <url>`
4. Default: `https://github.com/kreitter/workato-sdk-docs.git`

## Troubleshooting

### HTML Parsing Failures
```bash
# Identify which URLs fail
uv run python scripts/fetch_workato_docs.py

# Test single URL extraction
python3 -c "from scripts.fetch_workato_docs import WorkatoDocsConverter; import sys; sys.exit(0 if WorkatoDocsConverter().test_url('URL_HERE') else 1)"

# Update selectors in extract_main_content() if HTML structure changed
```

### Installation Issues
```bash
# Modern installation (handles PEP 668)
uvx --from git+https://github.com/kreitter/workato-sdk-docs.git workato-sdk-install

# Manual cleanup if needed
rm -rf ~/.workato-sdk-docs
rm -f ~/.claude/commands/workato-sdk.md
```

### Claude Command Not Working
```bash
# Check if command exists
ls ~/.claude/commands/workato-sdk.md

# Verify helper script is executable
ls -la ~/.workato-sdk-docs/workato-sdk-helper.sh

# Restart Claude Code after installation
```

## Development Workflow

### Adding New Documentation URLs
```python
# Edit scripts/fetch_workato_docs.py lines 36-127
SDK_URLS = [
    # ... existing URLs ...
    "https://docs.workato.com/en/developing-connectors/sdk/new-page.html",  # Add here
]
```

### Testing Changes
```bash
# Test import
python3 -c "from scripts.fetch_workato_docs import WorkatoDocsConverter"

# Test single URL
uv run python -c "from scripts.fetch_workato_docs import WorkatoDocsConverter; WorkatoDocsConverter().convert_single('URL')"

# Full fetch test
uv run python scripts/fetch_workato_docs.py

# Installation test
uvx --from . workato-sdk-install  # From repo root
```

### GitHub Actions Updates
- Schedule: `.github/workflows/update-docs.yml` line 6 (cron expression)
- Runs daily at 02:00 UTC
- Creates issues on failures with `bug`, `automation`, `sdk-docs` labels
- Commits with descriptive messages listing changed files

## Technical Details

### File Naming Convention
- Paths flattened with double underscores: `/guides/auth/oauth.html` → `guides__auth__oauth.md`
- Extension changed from `.html` to `.md`
- Special characters sanitized

### Rate Limiting
- 1-second delay between requests (`RATE_LIMIT_DELAY`)
- Exponential backoff on failures (2s initial, 30s max)
- 3 retry attempts per URL

### Content Hashing
- SHA-256 hash of content stored in `docs_manifest.json`
- Skip re-processing if content unchanged
- Track last fetch time and status per URL
