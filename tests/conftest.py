"""
Pytest configuration and shared fixtures for Workato SDK Documentation Mirror tests.
"""

import tempfile
from pathlib import Path

import pytest


@pytest.fixture
def temp_dir():
    """Provide a temporary directory for tests."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def sample_manifest():
    """Provide a sample manifest for testing."""
    return {
        "files": {
            "test.md": {
                "original_url": "https://example.com/test.html",
                "hash": "abc123def456",
                "last_updated": "2023-01-01T00:00:00",
            }
        },
        "fetch_metadata": {
            "last_fetch_completed": "2023-01-01T00:00:00",
            "pages_processed": 1,
            "pages_saved_successfully": 1,
            "pages_failed": 0,
        },
        "last_updated": "2023-01-01T00:00:00",
    }


@pytest.fixture
def mock_html_response():
    """Provide mock HTML response for testing."""
    return """
    <!DOCTYPE html>
    <html>
    <head><title>Test Page</title></head>
    <body>
        <header>Navigation</header>
        <main>
            <h1>Test Content</h1>
            <p>This is test content for parsing.</p>
            <ul>
                <li>List item 1</li>
                <li>List item 2</li>
            </ul>
            <pre><code>def test_function(): pass</code></pre>
        </main>
        <footer>Footer</footer>
    </body>
    </html>
    """


@pytest.fixture
def mock_session():
    """Provide a mock requests session."""

    class MockSession:
        def __init__(self):
            self.get_called = False
            self.last_url = None
            self.last_headers = None

        def get(self, url, headers=None, timeout=None):
            self.get_called = True
            self.last_url = url
            self.last_headers = headers
            self.last_timeout = timeout

            # Mock response
            class MockResponse:
                def __init__(self, text, status_code=200):
                    self.text = text
                    self.status_code = status_code

                def raise_for_status(self):
                    if self.status_code >= 400:
                        raise Exception(f"HTTP {self.status_code}")

            return MockResponse(mock_html_response(), 200)

    return MockSession()


@pytest.fixture
def workato_docs_converter():
    """Provide a WorkatoDocsConverter instance for testing."""
    from scripts.fetch_workato_docs import WorkatoDocsConverter

    return WorkatoDocsConverter()


@pytest.fixture
def sample_workato_html():
    """Provide sample Workato HTML content."""
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Authentication - Workato SDK</title>
    </head>
    <body>
        <nav class="navbar">Navigation</nav>
        <main class="main-content">
            <div class="container">
                <h1>Authentication Guide</h1>
                <p>Learn how to configure authentication for your connectors.</p>

                <section>
                    <h2>API Key Authentication</h2>
                    <p>Use API keys for simple authentication.</p>
                    <pre><code>{
  "authorization": {
    "type": "api_key",
    "api_key": "your-key-here"
  }
}</code></pre>
                </section>

                <section>
                    <h2>OAuth 2.0</h2>
                    <p>Implement OAuth 2.0 for secure authentication.</p>
                </section>
            </div>
        </main>
        <aside class="sidebar">Table of contents</aside>
    </body>
    </html>
    """


@pytest.fixture
def sample_urls():
    """Provide sample SDK URLs for testing."""
    return [
        "https://docs.workato.com/en/developing-connectors/sdk/cli.html",
        "https://docs.workato.com/en/developing-connectors/sdk/guides/authentication.html",
        "https://docs.workato.com/en/developing-connectors/sdk/sdk-reference.html",
    ]


@pytest.fixture
def mock_failed_response():
    """Provide a mock response that simulates network failure."""

    class MockFailedResponse:
        def __init__(self, exception_to_raise):
            self.exception = exception_to_raise

        def raise_for_status(self):
            raise self.exception

    return MockFailedResponse


@pytest.fixture
def test_fixtures_dir():
    """Provide the path to test fixtures directory."""
    return Path(__file__).parent / "fixtures"
