# Workato SDK Documentation Mirror

[![Last Update](https://img.shields.io/github/last-commit/kreitter/workato-sdk-docs/main.svg?label=docs%20updated)](https://github.com/kreitter/workato-sdk-docs/commits/main)
[![CI](https://github.com/kreitter/workato-sdk-docs/actions/workflows/test.yml/badge.svg)](https://github.com/kreitter/workato-sdk-docs/actions/workflows/test.yml)
[![Coverage](https://codecov.io/gh/kreitter/workato-sdk-docs/branch/main/graph/badge.svg)](https://codecov.io/gh/kreitter/workato-sdk-docs)
[![Python](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Platform](https://img.shields.io/badge/platform-macOS%20%7C%20Linux-blue)]()
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

Local mirror of Workato Connector SDK documentation, updated daily via GitHub Actions. Provides offline access to 90 SDK docs with Claude Code integration via `/workato-sdk` command.

## 🚀 Quick Start

### Prerequisites
- **Claude Code** ([install here](https://claude.ai/code))
- **Python 3.10+** (required for modern type hints and match statements)

### Installation

```bash
# One-liner installation with uvx
uvx --from git+https://github.com/kreitter/workato-sdk-docs.git workato-sdk-install
```

This command:
1. Installs the documentation to `~/.workato-sdk-docs`
2. Enables the `/workato-sdk` command in Claude Code
3. Fetches the latest documentation

## 🧪 Testing

```bash
# Run all tests
make test

# Run with coverage report
make coverage

# Run fast tests for quick feedback
make test-fast
```

Tests run automatically via pre-commit hooks and GitHub Actions. The test suite maintains 80% minimum code coverage.

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

1. **Fetches** 90 hardcoded SDK URLs from Workato docs
2. **Converts** HTML to Markdown using BeautifulSoup + html2text
3. **Stores** locally with content hashing for change detection
4. **Integrates** with Claude Code via `/workato-sdk` command
5. **Updates** daily via GitHub Actions (02:00 UTC)

## 🔄 Updates

- **Automatic**: GitHub Actions runs daily at 02:00 UTC
- **Manual**: Re-run the installer to refresh:
  ```bash
  uvx --from git+https://github.com/kreitter/workato-sdk-docs.git workato-sdk-install
  ```



## 🐛 Troubleshooting

- **Command not found**: Restart Claude Code after installation
- **Outdated docs**: Run `/workato-sdk -t` to check status
- **Parsing errors**: May indicate Workato changed HTML structure (file an issue)

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

### Setup

```bash
# Clone repository
git clone https://github.com/kreitter/workato-sdk-docs.git
cd workato-sdk-docs

# Install development dependencies
make install-dev

# Set up pre-commit hooks
make setup-precommit
```

### Development Workflow

```bash
# Install dev dependencies and pre-commit hooks
make install-dev
make setup-precommit

# During development
make test-fast  # Quick validation
make format     # Auto-format code
make lint       # Check code quality

# Before committing
make test       # Full test suite
make coverage   # Verify coverage threshold
```

### Contributing

- Add new URLs to `SDK_URLS` list in `fetch_workato_docs.py` (lines 202-410)
- Test changes with `uv run python scripts/fetch_workato_docs.py`
- Submit pull request

### Using Forks

The installer auto-detects forked repositories. Override with:
- Environment: `WORKATO_SDK_REPO_URL="https://github.com/yourfork.git"`
- Flag: `workato-sdk-install --repo <url>`

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

- **Version**: 3.1.0 | **Python**: 3.10+ | **Docs**: 90 SDK pages
- **Compatibility**: macOS, Linux | All Claude Code versions
