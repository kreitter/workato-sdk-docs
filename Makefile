# Makefile for Workato SDK Documentation Mirror

.PHONY: help test test-unit test-integration test-all install-dev lint format clean

# Default target
help:
	@echo "Available commands:"
	@echo "  test              Run all tests"
	@echo "  test-unit         Run unit tests only"
	@echo "  test-integration  Run integration tests only"
	@echo "  test-regression   Run regression tests only"
	@echo "  test-performance  Run performance tests only"
	@echo "  test-fast         Run unit + regression tests (fast)"
	@echo "  install-dev       Install development dependencies"
	@echo "  lint              Run linting checks"
	@echo "  format            Format code with black and isort"
	@echo "  coverage          Run tests with coverage report"
	@echo "  clean             Clean temporary files"
	@echo "  setup-precommit   Set up pre-commit hooks"

# Test commands
test:
	uv run pytest tests/ -v

test-unit:
	uv run pytest tests/test_unit_*.py -v

test-integration:
	uv run pytest tests/test_integration_*.py -v --timeout=60

test-regression:
	uv run pytest tests/test_regression_*.py -v

test-performance:
	uv run pytest tests/test_performance.py -v --durations=10

test-fast:
	uv run pytest tests/test_unit_*.py tests/test_regression_*.py -v

# Development commands
install-dev:
	uv sync --dev

lint:
	uv run flake8 --max-line-length=100 --ignore=E203,W503 scripts/ workato_sdk_docs/ tests/
	uv run black --check scripts/ workato_sdk_docs/ tests/
	uv run isort --check-only scripts/ workato_sdk_docs/ tests/

format:
	uv run black scripts/ workato_sdk_docs/ tests/
	uv run isort scripts/ workato_sdk_docs/ tests/

coverage:
	uv run pytest tests/ --cov=scripts --cov=workato_sdk_docs --cov-report=html --cov-report=term

clean:
	find . -type d -name __pycache__ -delete
	find . -type f -name "*.pyc" -delete
	rm -rf .pytest_cache/
	rm -rf .coverage
	rm -rf htmlcov/
	rm -rf .tox/

setup-precommit:
	pip install pre-commit
	pre-commit install
