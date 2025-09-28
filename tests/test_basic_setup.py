"""
Basic test to verify the testing framework is properly set up.
"""

import sys
from pathlib import Path


def test_python_version():
    """Test that we're running a compatible Python version."""
    assert sys.version_info >= (
        3,
        10,
    ), f"Python {sys.version_info.major}.{sys.version_info.minor} is not supported"


def test_project_structure():
    """Test that the project structure is correct."""
    project_root = Path(__file__).parent.parent

    # Check core directories exist
    assert (project_root / "scripts").exists(), "scripts directory missing"
    assert (project_root / "workato_sdk_docs").exists(), "workato_sdk_docs directory missing"
    assert (project_root / "docs").exists(), "docs directory missing"

    # Check core files exist
    assert (
        project_root / "scripts" / "fetch_workato_docs.py"
    ).exists(), "fetch_workato_docs.py missing"
    assert (project_root / "workato_sdk_docs" / "installer.py").exists(), "installer.py missing"
    assert (project_root / "pyproject.toml").exists(), "pyproject.toml missing"


def test_test_fixtures_exist():
    """Test that test fixtures are available."""
    fixtures_dir = Path(__file__).parent / "fixtures"
    assert fixtures_dir.exists(), "fixtures directory missing"

    sample_html_dir = fixtures_dir / "sample_html"
    assert sample_html_dir.exists(), "sample_html fixtures directory missing"

    # Check for sample HTML files
    html_files = list(sample_html_dir.glob("*.html"))
    assert len(html_files) > 0, "No sample HTML files found"


def test_imports_work():
    """Test that we can import the modules we're testing."""
    try:
        from scripts.fetch_workato_docs import WorkatoDocsConverter, url_to_filename
        from workato_sdk_docs.installer import main as installer_main

        # Use the imports to avoid F401 warnings
        converter = WorkatoDocsConverter()  # noqa: F841
        filename = url_to_filename("https://example.com/test.html")  # noqa: F841
        assert callable(installer_main)

        assert True, "Imports successful"
    except ImportError as e:
        assert False, f"Import failed: {e}"


def test_url_to_filename_function():
    """Test the URL to filename conversion function."""
    from scripts.fetch_workato_docs import url_to_filename

    # Test basic functionality
    url = "https://docs.workato.com/en/developing-connectors/sdk/cli.html"
    result = url_to_filename(url)
    assert result == "cli.md", f"Expected 'cli.md', got '{result}'"

    # Test with nested paths
    url = "https://docs.workato.com/en/developing-connectors/sdk/guides/authentication/api-key.html"
    result = url_to_filename(url)
    assert result == "guides__authentication__api-key.md", f"Unexpected result: {result}"

    # Test without .html extension
    url = "https://docs.workato.com/en/developing-connectors/sdk/cli"
    result = url_to_filename(url)
    assert result == "cli.md", f"Expected 'cli.md', got '{result}'"
