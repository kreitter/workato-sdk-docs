# WARP.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

## Repository Overview

This is a documentation mirror system that automatically fetches Workato SDK HTML documentation and converts it to Markdown for local access in Claude Code. The system provides the `/workato-sdk` command integration for developers working with Workato Connector SDK.

## Essential Commands

### Development & Testing
```bash
# Test the documentation fetcher (downloads and converts 90+ Workato SDK docs)
python3 scripts/fetch_workato_docs.py

# Run all implementation tests
./test_implementation.sh

# Install Python dependencies
pip3 install --user --break-system-packages -r scripts/requirements.txt

# Test full installation locally
./install.sh

# Manual update of documentation cache
cd ~/.workato-sdk-docs && python3 scripts/fetch_workato_docs.py
```

### GitHub Actions & Deployment
```bash
# Trigger manual documentation update workflow
gh workflow run update-docs.yml

# View workflow execution history
gh run list --workflow=update-docs.yml

# Check workflow logs for debugging
gh run view <run-id> --log
```

## Architecture & Core Components

### Documentation Processing Pipeline
The system uses a multi-stage approach fundamentally different from typical Markdown-based documentation mirrors:

1. **Direct URL Fetching**: Uses hardcoded list of 90 SDK URLs in `scripts/fetch_workato_docs.py`
2. **HTML Extraction**: `WorkatoDocsConverter` class extracts main content using BeautifulSoup
3. **Markdown Conversion**: Converts HTML to clean Markdown using html2text
4. **Local Storage**: Saves to `docs/` directory with content hashing for change detection
5. **Command Integration**: Bash script provides `/workato-sdk` command interface for Claude Code

### Key Files & Responsibilities
```
scripts/fetch_workato_docs.py          # Core HTML fetcher and converter
scripts/workato-sdk-helper.sh.template # Command handler template
scripts/requirements.txt               # Python dependencies
install.sh                            # One-command installation
.github/workflows/update-docs.yml      # Daily auto-update workflow
docs/                                 # Converted Markdown files
docs_manifest.json                    # Metadata and change tracking
```

## Critical Implementation Details

### HTML Content Extraction Strategy
When Workato changes their documentation structure, update CSS selectors in `extract_main_content()`:

```python
selectors = [
    'main.content',
    'div.content', 
    'article.doc-content',
    'div.doc-body',
    # Add new selectors here if Workato changes HTML structure
]
```

### URL Management System
The `SDK_URLS` list (lines 36-127 in `fetch_workato_docs.py`) contains all documentation pages:
- Currently includes 90 SDK documentation URLs
- Manually curated to avoid external dependencies
- Excludes import-via-oas pages that aren't SDK-specific
- Use `is_sdk_url()` only for fallback crawling scenarios

### Repository Configuration Requirements
**CRITICAL**: Before deployment, update these hardcoded values:
- `install.sh` line 17: Update `REPO_URL` from `kreitter` to actual GitHub username
- `README.md`: Replace all GitHub URLs with correct repository
- `scripts/workato-sdk-helper.sh.template`: Update GitHub repository references

## Common Troubleshooting Scenarios

### HTML Structure Changes
If Workato updates their documentation design:
1. Run `python3 scripts/fetch_workato_docs.py` to identify parsing failures
2. Inspect failing URLs in browser to identify new HTML structure
3. Update `extract_main_content()` selectors in `WorkatoDocsConverter` class
4. Test with single URL before running full fetch

### Content Conversion Issues
- Modify html2text configuration in `WorkatoDocsConverter.__init__()`
- Update `post_process_markdown()` for cleanup rules
- Check for JavaScript-rendered content (may require different extraction approach)

### Installation Problems
- Verify all dependencies: `git`, `jq`, `curl`, `python3`
- Check Python packages: `pip3 install requests beautifulsoup4 html2text`
- Ensure proper file permissions on scripts
- Clear existing installations if corrupted: `rm -rf ~/.workato-sdk-docs`

## Development Workflow

### Testing Strategy
Always test in this sequence:
1. **Python Import Test**: `python3 -c "from scripts.fetch_workato_docs import WorkatoDocsConverter"`
2. **Single URL Test**: Temporarily modify `SDK_ENTRY_POINTS` to test one URL
3. **Full Fetch Test**: Run complete documentation fetch
4. **Installation Test**: Verify `install.sh` creates all components correctly

### Adding New Documentation Sections
1. Add URLs to `SDK_URLS` list in `scripts/fetch_workato_docs.py`
2. Test fetching: `python3 scripts/fetch_workato_docs.py`
3. Verify new files appear in `docs/` directory
4. Check conversion quality in generated Markdown

### GitHub Actions Workflow
- Runs daily at 02:00 UTC (less frequent than typical docs due to SDK stability)
- Automatically commits changes when documentation updates
- Creates GitHub issues on fetch failures
- Modify schedule by changing cron expression in `update-docs.yml` line 6

## File Naming Convention

URLs are flattened to avoid deep directory structures:
- `/en/developing-connectors/sdk/sdk-reference.html` → `sdk-reference.md`
- Nested paths use double underscores: `guides/auth/oauth.html` → `guides__auth__oauth.md`

## Rate Limiting & Reliability

- 1-second delay between requests to respect Workato's servers
- Retry logic with exponential backoff for failed requests
- Content hashing prevents unnecessary re-processing of unchanged pages
- Manifest file tracks fetch metadata and change history

## Integration Points

The system integrates with Claude Code through:
- `/workato-sdk` command installed to `~/.claude/commands/`
- Auto-update hooks for keeping documentation current
- Search capabilities across all SDK documentation
- Direct linking back to official Workato documentation pages

## Maintenance Requirements

### Regular Updates
- Monitor GitHub Actions workflow for failures
- Update `SDK_URLS` list when Workato adds new documentation sections
- Adjust HTML parsing selectors when Workato redesigns their documentation

### Version Management
- Script versioning in `workato-sdk-helper.sh.template`
- Dependency versioning in `requirements.txt`
- Branch management for stable vs development versions

## Security Considerations

- Input sanitization in bash scripts prevents command injection
- Rate limiting respects Workato's server resources  
- No API keys or authentication required (public documentation only)
- Git-based version control provides audit trail for all changes
