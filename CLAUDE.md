# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Purpose

This is a documentation mirror system that fetches Workato SDK HTML documentation and converts it to Markdown for local access in Claude Code. It's adapted from claude-code-docs but with significant architectural differences due to Workato only providing HTML (not Markdown) documentation.

## Essential Commands

### Development & Testing
```bash
# Test the fetcher (downloads and converts Workato SDK docs)
python3 scripts/fetch_workato_docs.py

# Run implementation tests
./test_implementation.sh

# Install Python dependencies
pip3 install --user --break-system-packages -r scripts/requirements.txt

# Test installation locally
./install.sh

# Manual documentation update
cd ~/.workato-sdk-docs && python3 scripts/fetch_workato_docs.py
```

### GitHub Actions
```bash
# Trigger manual workflow run
gh workflow run update-docs.yml

# View workflow runs
gh run list --workflow=update-docs.yml
```

## Architecture Overview

### Documentation Fetching Pipeline

Unlike claude-code-docs which fetches Markdown directly, this system must:

1. **URL List Processing** 
   - Uses hardcoded list of 90 SDK URLs in `SDK_URLS` constant
   - No external dependencies on sitemaps or web services
   - Comprehensive coverage of all SDK documentation pages
   - Fallback to crawling only if URL list is empty (unlikely)

2. **HTML to Markdown Conversion** (`WorkatoDocsConverter` class)
   - Extracts main content from HTML using BeautifulSoup
   - Removes navigation, headers, footers, scripts
   - Converts HTML to Markdown using html2text
   - Post-processes to clean conversion artifacts

### Key Components Integration

```
fetch_workato_docs.py (Python)
    ↓ Generates docs/*.md files
install.sh (Bash)
    ↓ Creates workato-sdk-helper.sh from template
workato-sdk-helper.sh (Bash)
    ↓ Provides /workato-sdk command
Claude Code Integration
```

## Critical Implementation Details

### HTML Content Extraction (`scripts/fetch_workato_docs.py`)

The `extract_main_content()` method tries multiple CSS selectors to find documentation content. When Workato changes their HTML structure, update these selectors:

```python
selectors = [
    'main.content',
    'div.content',
    'article.doc-content',
    # Add new selectors here if structure changes
]
```

### URL List Management

The `SDK_URLS` list contains all documentation pages to fetch. The `is_sdk_url()` method is only used as a fallback for the deprecated crawling approach.

### Repository Configuration

**IMPORTANT**: Update these before deployment:
- `install.sh` line 17: `REPO_URL="https://github.com/kreitter/workato-sdk-docs.git"`
- `README.md`: Replace all instances of `kreitter` with actual GitHub username
- `scripts/workato-sdk-helper.sh.template`: Update GitHub URLs

## Common Issues & Solutions

### HTML Structure Changes
If Workato changes their documentation HTML:
1. Run fetcher to see what fails: `python3 scripts/fetch_workato_docs.py`
2. Inspect Workato's HTML to find new content selectors
3. Update `extract_main_content()` selectors in `fetch_workato_docs.py`
4. Test with single page before full fetch

### URL Updates
- To add new documentation pages, update the `SDK_URLS` list in `fetch_workato_docs.py`
- The list is hardcoded to avoid external dependencies
- Last updated: 2025-08-14 with 90 SDK documentation URLs (excludes import-via-oas pages)

### Conversion Problems
- Update html2text configuration in `WorkatoDocsConverter.__init__()`
- Adjust `post_process_markdown()` for cleanup rules
- Check for JavaScript-rendered content (may need different approach)

## Testing Approach

Always test in this order:
1. Python imports: `python3 -c "from scripts.fetch_workato_docs import WorkatoDocsConverter"`
2. Single page fetch: Temporarily modify `SDK_ENTRY_POINTS` to one URL
3. Full crawl: Run complete fetcher
4. Installation: Test `install.sh` creates all components correctly

## GitHub Actions Workflow

The workflow (`update-docs.yml`) runs daily and:
1. Fetches latest SDK documentation
2. Commits changes if any
3. Creates issue on failure

To modify schedule, change cron expression on line 6.

## File Naming Convention

URLs are converted to flat filenames:
- `/en/developing-connectors/sdk/sdk-reference.html` → `sdk-reference.md`
- Subdirectories use double underscores: `advanced/setup.html` → `advanced__setup.md`

This avoids deep nesting in the local docs/ directory.