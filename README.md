# Workato SDK Documentation Mirror

[![Last Update](https://img.shields.io/github/last-commit/kreitter/workato-sdk-docs/main.svg?label=docs%20updated)](https://github.com/kreitter/workato-sdk-docs/commits/main)
[![CI](https://github.com/kreitter/workato-sdk-docs/actions/workflows/test.yml/badge.svg)](https://github.com/kreitter/workato-sdk-docs/actions/workflows/test.yml)
[![Coverage](https://codecov.io/gh/kreitter/workato-sdk-docs/branch/main/graph/badge.svg)](https://codecov.io/gh/kreitter/workato-sdk-docs)
[![Python](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Platform](https://img.shields.io/badge/platform-macOS%20%7C%20Linux-blue)]()
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

Access 90 Workato SDK documentation pages directly in Claude Code with the `/workato-sdk` command. Updated daily via GitHub Actions.

## 🚀 Quick Start

### Prerequisites
- **Claude Code** ([install here](https://claude.ai/code))
- **Python 3.10+**

### Installation

```bash
uvx --from git+https://github.com/kreitter/workato-sdk-docs.git workato-sdk-install
```

This installs documentation locally and enables the `/workato-sdk` command in Claude Code.

## 📖 Usage

```bash
# List all available SDK documentation
/workato-sdk

# Read specific documentation
/workato-sdk sdk-reference
/workato-sdk authentication

# Natural language queries
/workato-sdk how do I create a custom connector?
/workato-sdk explain connection configuration

# Check sync status
/workato-sdk -t
```

## 🔄 Updates

- **Automatic**: Daily via GitHub Actions (02:00 UTC)
- **Manual**: Re-run the installer:
  ```bash
  uvx --from git+https://github.com/kreitter/workato-sdk-docs.git workato-sdk-install
  ```

## 🐛 Troubleshooting

- **Command not found**: Restart Claude Code after installation
- **Outdated docs**: Re-run the installer or check `/workato-sdk -t`
- **Issues**: Report at [GitHub Issues](https://github.com/kreitter/workato-sdk-docs/issues)

## 🗑️ Uninstalling

```bash
~/.workato-sdk-docs/uninstall.sh
```

## 🤝 Contributing

See [CLAUDE.md](CLAUDE.md) for development setup and guidelines.

To use a fork:
```bash
export WORKATO_SDK_REPO_URL="https://github.com/yourfork.git"
uvx --from $WORKATO_SDK_REPO_URL workato-sdk-install
```

## ⚠️ Disclaimer

This is an unofficial tool not affiliated with Workato, Inc. It's a community project to improve developer experience with Workato SDK documentation in Claude Code.

Workato documentation content belongs to Workato, Inc.

## 🔗 Links

- [Official Workato SDK Documentation](https://docs.workato.com/en/developing-connectors/sdk.html)
- [Workato Developers Program](https://www.workato.com/developers)
- [Claude Code](https://claude.ai/code)

---

**Version**: 3.1.0 | **License**: MIT | **Pages**: 90 SDK docs
