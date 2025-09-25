# Workato SDK Documentation Mirror

[![Last Update](https://img.shields.io/github/last-commit/kreitter/workato-sdk-docs/main.svg?label=docs%20updated)](https://github.com/kreitter/workato-sdk-docs/commits/main)
[![Platform](https://img.shields.io/badge/platform-macOS%20%7C%20Linux-blue)]()
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

Local mirror of Workato Connector SDK documentation from https://docs.workato.com/en/developing-connectors/sdk/, updated daily via GitHub Actions.

## 🎯 Purpose

This tool provides:
- **Local access** to Workato SDK documentation within Claude Code
- **Offline availability** of SDK reference materials
- **Automatic updates** to stay current with official docs
- **Fast searching** across all SDK documentation
- **Markdown format** for better readability in CLI

## ✨ Features

- 📚 Complete Workato Connector SDK documentation
- 🔄 Daily automatic updates via GitHub Actions
- 🔍 Fast local search capabilities
- 📖 Markdown conversion from HTML docs
- 🛠️ Integration with Claude Code via `/workato-sdk` command
- 📊 Change tracking and version history

## 🚀 Quick Start

### Installation

Recommended (one-liner with uvx)

```bash
# Install/enable Workato SDK Docs and the /workato-sdk command (if Claude is installed)
uvx --from git+https://github.com/kreitter/workato-sdk-docs.git workato-sdk-install
```

Alternative (developer workflow; runs locally with uv)

```bash
# macOS: install uv
brew install uv

# Run the fetcher in an isolated environment (avoids PEP 668)
uv run python scripts/fetch_workato_docs.py
```

Note: The old installer (install.sh) is deprecated in favor of uv-based installation.

### Prerequisites

- **Claude Code** - The CLI tool this integrates with ([install here](https://claude.ai/code))
- **git** - For cloning and updating the repository
- **curl** - For downloading the installation script (usually pre-installed)
- **python3** - Version 3.8 or higher

Python dependencies (installed automatically):
- `requests` - For HTTP requests
- `beautifulsoup4` - For HTML parsing
- `html2text` - For HTML to Markdown conversion

## 📖 Usage

### Basic Commands

```bash
# List all available SDK documentation topics
/workato-sdk

# Read specific SDK documentation
/workato-sdk sdk-reference
/workato-sdk platform-quickstart

# Check sync status with GitHub
/workato-sdk -t

# See recent documentation updates
/workato-sdk what's new

# Get uninstall instructions
/workato-sdk uninstall
```

### Example Usage

```bash
# Read about SDK reference
/workato-sdk sdk-reference

# Search for authentication topics
/workato-sdk authentication

# Check if docs are up-to-date
/workato-sdk -t

# Natural language queries work too
/workato-sdk how do I create a custom connector?
/workato-sdk explain connection configuration
```

## 🔧 How It Works

### Architecture

1. **Direct Fetching**: Python script fetches from hardcoded list of 90 SDK documentation URLs
2. **Conversion**: BeautifulSoup + html2text convert HTML to Markdown
3. **Storage**: Docs saved locally with content hashing for change detection
4. **Integration**: Shell script provides Claude Code command interface
5. **Updates**: GitHub Actions runs daily to fetch latest docs

### Components

```
workato-sdk-docs/
├── scripts/
│   ├── fetch_workato_docs.py      # Main fetcher/converter
│   ├── workato-sdk-helper.sh      # Command handler
│   └── requirements.txt           # Python dependencies
├── docs/                           # Converted documentation
│   └── *.md                       # Markdown files
├── install.sh                      # Installation script
├── uninstall.sh                   # Uninstallation script
└── .github/workflows/
    └── update-docs.yml            # GitHub Actions workflow
```

## 🔄 Updates

### Automatic Updates

- GitHub Actions runs daily at 02:00 UTC
- Fetches latest documentation from Workato
- Commits changes automatically
- Creates issues on failures

### Manual Updates

To manually update the documentation:

```bash
uv run python scripts/fetch_workato_docs.py
```

Or re-run the installer to refresh and reconfigure Claude integration:

```bash
uvx --from git+https://github.com/kreitter/workato-sdk-docs.git workato-sdk-install
```

## 🔍 Advanced Features

### Search Across All Docs

```bash
# Search for a term across all SDK documentation
cd ~/.workato-sdk-docs
grep -r "authentication" docs/

# Find files containing specific patterns
grep -l "custom connector" docs/*.md
```

### View Change History

```bash
# See recent changes
cd ~/.workato-sdk-docs
git log --oneline -10 -- docs/

# View specific changes
git diff HEAD~1 -- docs/sdk-reference.md
```

## 🛠️ Configuration

### Customizing the Fetcher

Edit `scripts/fetch_workato_docs.py` to:
- Add or remove SDK pages from the `SDK_URLS` list
- Modify HTML parsing rules
- Change rate limiting
- Update content extraction selectors

### Repository Settings

The installer accepts the repository URL via env or flags:
1. Environment variable: `WORKATO_SDK_REPO_URL`
2. Flag override: `workato-sdk-install --repo <url>`
3. Default: `https://github.com/kreitter/workato-sdk-docs.git`

```bash
# Using a fork with auto-detection
git clone https://github.com/yourusername/workato-sdk-docs.git
cd workato-sdk-docs
./install.sh  # Automatically uses your fork

# Or override with environment variable
WORKATO_SDK_REPO_URL="https://github.com/yourusername/workato-sdk-docs.git" \
  bash -c "$(curl -fsSL https://raw.githubusercontent.com/kreitter/workato-sdk-docs/main/install.sh)"
```

To change the branch, edit `INSTALL_BRANCH` in `install.sh`

## 🐛 Troubleshooting

### Command not found

If `/workato-sdk` returns "command not found":
1. Check if command exists: `ls ~/.claude/commands/workato-sdk.md`
2. Restart Claude Code
3. Re-run installation script

### Documentation not updating

If documentation seems outdated:
1. Run `/workato-sdk -t` to check sync status
2. Manually update: `cd ~/.workato-sdk-docs && git pull`
3. Re-fetch docs: `python3 scripts/fetch_workato_docs.py`

### HTML parsing errors

If conversion fails:
1. Check Workato hasn't changed their HTML structure
2. Review logs: `cd ~/.workato-sdk-docs && python3 scripts/fetch_workato_docs.py`
3. Update BeautifulSoup selectors in fetcher script

## 🗑️ Uninstalling

To completely remove the SDK docs integration:

```bash
/workato-sdk uninstall
# Then run the displayed command
```

Or directly:
```bash
~/.workato-sdk-docs/uninstall.sh
```

This removes:
- The `/workato-sdk` command
- Auto-update hooks
- Installation directory

## 📝 Development

### Setting Up Development Environment

```bash
# Fork and clone the repository
git clone https://github.com/kreitter/workato-sdk-docs.git
cd workato-sdk-docs

# Install uv if not already installed
# macOS: brew install uv
# Linux: curl -LsSf https://astral.sh/uv/install.sh | sh

# Test the fetcher with uv (auto-installs dependencies)
uv run python scripts/fetch_workato_docs.py

# Test installation
uvx --from . workato-sdk-install --no-claude
```

### Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

### Adding New Documentation Sources

To add more Workato documentation:

1. Edit `SDK_URLS` list in `fetch_workato_docs.py` (lines 37-128)
2. Add the full URL for each new documentation page
3. Test fetching: `python3 scripts/fetch_workato_docs.py`

## 📄 License

This tool is MIT licensed. See [LICENSE](LICENSE) file.

Workato documentation content belongs to Workato, Inc.

## 🤝 Acknowledgments

- Inspired by [claude-code-docs](https://github.com/ericbuess/claude-code-docs)
- Built for the Claude Code community
- Thanks to Workato for their comprehensive SDK documentation

## ⚠️ Disclaimer

This is an unofficial tool not affiliated with Workato, Inc. It's a community project to improve developer experience when working with Workato SDK documentation in Claude Code.

## 🔗 Links

- [Official Workato SDK Documentation](https://docs.workato.com/en/developing-connectors/sdk.html)
- [Workato Developers Program](https://www.workato.com/developers)
- [Claude Code](https://claude.ai/code)

## 📊 Status

- **Version**: 3.1.0
- **Last Updated**: 2025-09-24
- **Compatibility**: macOS, Linux
- **Python**: 3.10+
- **Claude Code**: All versions

---

**Note**: The installer automatically detects forked repositories. No manual URL updates needed!
