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

Run this single command:

```bash
curl -fsSL https://raw.githubusercontent.com/kreitter/workato-sdk-docs/main/install.sh | bash
```

This will:
1. Install to `~/.workato-sdk-docs`
2. Create the `/workato-sdk` slash command in Claude Code
3. Set up automatic updates
4. Fetch the latest SDK documentation

### Prerequisites

- **git** - For cloning and updating the repository
- **jq** - For JSON processing (install with `apt install jq` or `brew install jq`)
- **curl** - For downloading the installation script
- **python3** - For fetching and converting documentation
- **Claude Code** - The CLI tool this integrates with

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
cd ~/.workato-sdk-docs
python3 scripts/fetch_workato_docs.py
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

Update these in `install.sh`:
- `REPO_URL` - Your GitHub repository
- `INSTALL_BRANCH` - Branch to install from

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

# Install Python dependencies
pip3 install -r scripts/requirements.txt

# Test the fetcher
python3 scripts/fetch_workato_docs.py

# Test installation
./install.sh
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

- **Version**: 3.0.0
- **Last Updated**: 2025-08-14
- **Compatibility**: macOS, Linux
- **Python**: 3.8+
- **Claude Code**: All versions

---

**Note**: Remember to update the repository URL in the installation script and README after creating your GitHub repository.