# Repository Guidelines

## Project Structure & Module Organization
`workato_sdk_docs/` contains the installable package and CLI entry point in `installer.py`. `scripts/` holds repository utilities, especially `fetch_workato_docs.py`, which fetches and converts the upstream Workato SDK pages. `docs/` is the generated Markdown mirror plus `docs_manifest.json`; treat it as generated output, not hand-authored source. `tests/` contains unit, integration, regression, and performance coverage. CI workflows live in `.github/workflows/`.

## Build, Test, and Development Commands
Use `uv` for environment management and `make` as the main task runner.

- `make install-dev`: install runtime and dev dependencies.
- `make test`: run the full pytest suite.
- `make test-fast`: run unit and regression tests for quick feedback.
- `make coverage`: run tests with coverage output in `htmlcov/`.
- `make lint`: run `flake8`, `black --check`, and `isort --check-only`.
- `make format`: auto-format Python files.
- `uv run python scripts/fetch_workato_docs.py`: refresh the mirrored docs and manifest.

## Coding Style & Naming Conventions
Target Python 3.10+ and use 4-space indentation. Format with Black, sort imports with isort using the Black profile, and keep lines at 100 characters. Lint with Flake8 (`E203,W503` ignored). Prefer descriptive snake_case for functions, modules, and test helpers. Keep generated docs filenames consistent with the current slug pattern, for example `guides__authentication__api-key.md`.

## Testing Guidelines
Pytest is the test runner, with `pytest-cov`, `pytest-mock`, `responses`, `requests-mock`, and `freezegun` used where appropriate. Follow the existing naming split: `test_unit_*.py`, `test_integration_*.py`, `test_regression_*.py`, and `test_performance.py`. Codecov targets 85% project coverage and 80% patch coverage, so run `make coverage` before large changes.

## Commit & Pull Request Guidelines
Match the repo’s existing history. Automated content syncs use `Update Workato SDK docs - YYYY-MM-DD | Updated: ...`; manual maintenance changes use concise prefixes like `chore:`. Keep commits focused and explain whether a PR changes generator logic, generated docs, or both. Link related issues, note any parser or network assumptions, and include representative command output when behavior changes. Screenshots are only useful if rendered Markdown output materially changes.

## Generated Content & Automation
Daily GitHub Actions refresh `docs/` and run the test matrix on Python 3.10-3.12. If you modify fetching or parsing logic, regenerate affected docs locally and include both code and output changes in the same PR.
