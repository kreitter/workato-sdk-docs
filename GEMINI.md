# Gemini CLI Context for `workato-sdk-docs`

## Project Overview
`workato-sdk-docs` is a Python-based utility that provides a local, offline mirror of Workato Connector SDK documentation. It is designed to integrate specifically with Claude Code, allowing developers to query up-to-date Workato documentation locally via the `/workato-sdk` command.

The tool works by fetching Workato SDK URLs, converting the HTML content to Markdown using `BeautifulSoup4` and `html2text`, and storing it locally with content hashing to track changes. Updates are automated daily via GitHub Actions.

## Building and Running

The project heavily relies on the `uv` package manager and a `Makefile` for local development workflows.

### Installation
- Install the tool globally: `uvx --from git+https://github.com/kreitter/workato-sdk-docs.git workato-sdk-install`
- Set up for local development: `make install-dev`
- Set up pre-commit hooks: `make setup-precommit`

### Testing
- Run all tests: `make test`
- Run fast tests (unit + regression): `make test-fast`
- Run with coverage report: `make coverage`

### Code Quality and Linting
- Auto-format code (`black` and `isort`): `make format`
- Run linting checks (`flake8`): `make lint`
- Clean temporary and cache files: `make clean`

## Development Conventions

- **Language:** Python 3.10+
- **Dependency Management:** `uv` (`pyproject.toml`)
- **Code Formatting:** `black` and `isort` are used for consistent styling.
- **Linting:** `flake8` is used for static analysis.
- **Testing Framework:** `pytest` is used across unit, integration, and performance tests. The project aims to maintain at least an 80% code coverage threshold.
- **Continuous Integration:** Changes should pass the pre-commit hooks (`make precommit-test`) before committing.
