"""
Unit tests for core functionality in fetch_workato_docs.py

Tests the fundamental parsing, conversion, and utility functions.
"""

import hashlib
import json
import tempfile
from pathlib import Path
from unittest.mock import Mock, patch

import pytest
import requests
from bs4 import BeautifulSoup

# Import the functions we want to test
from scripts.fetch_workato_docs import (
    HTTPError,
    NetworkError,
    WorkatoDocsConverter,
    fetch_page_content,
    load_manifest,
    save_manifest,
    url_to_filename,
)


class TestURLHandling:
    """Test URL parsing and filename generation."""

    def test_url_to_filename_basic(self):
        """Test basic URL to filename conversion."""
        url = "https://docs.workato.com/en/developing-connectors/sdk/cli.html"
        expected = "cli.md"
        assert url_to_filename(url) == expected

    def test_url_to_filename_with_path(self):
        """Test URL with nested paths."""
        url = (
            "https://docs.workato.com/en/developing-connectors/sdk/guides/"
            "authentication/api-key.html"
        )
        expected = "guides__authentication__api-key.md"
        assert url_to_filename(url) == expected

    def test_url_to_filename_with_query_params(self):
        """Test URL with query parameters."""
        url = "https://docs.workato.com/en/developing-connectors/sdk/sdk-reference.html?tab=actions"
        expected = "sdk-reference.md"
        assert url_to_filename(url) == expected

    def test_url_to_filename_with_fragment(self):
        """Test URL with fragment identifiers."""
        url = "https://docs.workato.com/en/developing-connectors/sdk/guides.html#building-actions"
        expected = "guides.md"
        assert url_to_filename(url) == expected

    def test_url_to_filename_edge_cases(self):
        """Test edge cases in URL parsing."""
        # Empty path
        url = "https://docs.workato.com"
        assert url_to_filename(url) == ".md"

        # Root path
        url = "https://docs.workato.com/"
        assert url_to_filename(url) == ".md"

        # Multiple slashes - they get collapsed to double underscores
        url = "https://docs.workato.com//en//developing-connectors//sdk//"
        result = url_to_filename(url)
        assert "en" in result
        assert "developing-connectors" in result
        assert "sdk" in result
        assert result.endswith(".md")


class TestContentHashing:
    """Test content hashing functionality."""

    def test_content_hashing_consistency(self):
        """Test that same content produces same hash."""
        content1 = "test content"
        content2 = "test content"
        hash1 = hashlib.sha256(content1.encode("utf-8")).hexdigest()
        hash2 = hashlib.sha256(content2.encode("utf-8")).hexdigest()
        assert hash1 == hash2

    def test_content_hashing_different_content(self):
        """Test that different content produces different hashes."""
        content1 = "test content 1"
        content2 = "test content 2"
        hash1 = hashlib.sha256(content1.encode("utf-8")).hexdigest()
        hash2 = hashlib.sha256(content2.encode("utf-8")).hexdigest()
        assert hash1 != hash2

    def test_content_hashing_encoding(self):
        """Test hashing with different encodings."""
        content = "test content with ümlaut"
        hash_utf8 = hashlib.sha256(content.encode("utf-8")).hexdigest()
        hash_latin1 = hashlib.sha256(content.encode("latin-1")).hexdigest()
        # Should be different due to encoding differences
        assert hash_utf8 != hash_latin1


class TestManifestOperations:
    """Test manifest loading and saving."""

    def test_load_manifest_nonexistent(self):
        """Test loading manifest when file doesn't exist."""
        with tempfile.TemporaryDirectory() as tmpdir:
            manifest_path = Path(tmpdir) / "manifest.json"
            manifest = load_manifest(manifest_path)
            assert manifest == {"files": {}, "last_updated": None}

    def test_load_manifest_empty_file(self):
        """Test loading manifest from empty file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            manifest_path = Path(tmpdir) / "manifest.json"
            manifest_path.write_text("")
            manifest = load_manifest(manifest_path)
            assert manifest == {"files": {}, "last_updated": None}

    def test_load_manifest_invalid_json(self):
        """Test loading manifest with invalid JSON."""
        with tempfile.TemporaryDirectory() as tmpdir:
            manifest_path = Path(tmpdir) / "manifest.json"
            manifest_path.write_text("invalid json content")
            manifest = load_manifest(manifest_path)
            assert manifest == {"files": {}, "last_updated": None}

    def test_load_manifest_valid(self):
        """Test loading valid manifest."""
        with tempfile.TemporaryDirectory() as tmpdir:
            docs_dir = Path(tmpdir)
            manifest_path = docs_dir / "docs_manifest.json"
            test_data = {
                "files": {"test.md": {"hash": "abc123"}},
                "last_updated": "2023-01-01T00:00:00",
            }
            manifest_path.write_text(json.dumps(test_data))

            manifest = load_manifest(docs_dir)
            assert manifest == test_data

    def test_save_manifest(self):
        """Test saving manifest to file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            docs_dir = Path(tmpdir)
            test_data = {
                "files": {"test.md": {"hash": "abc123"}},
                "last_updated": "2023-01-01T00:00:00",
            }

            save_manifest(docs_dir, test_data)
            manifest_path = docs_dir / "docs_manifest.json"
            assert manifest_path.exists()

            loaded = json.loads(manifest_path.read_text())
            assert "test.md" in loaded["files"]
            assert loaded["files"]["test.md"]["hash"] == "abc123"


class TestWorkatoDocsConverter:
    """Test HTML to Markdown conversion."""

    def test_converter_initialization(self):
        """Test converter initializes correctly."""
        converter = WorkatoDocsConverter()
        assert converter.h2t is not None
        assert converter.h2t.body_width == 0
        assert converter.h2t.protect_links is True

    def test_extract_main_content_basic_html(self):
        """Test content extraction from basic HTML."""
        converter = WorkatoDocsConverter()

        html = """
        <html>
        <head><title>Test</title></head>
        <body>
            <header>Navigation</header>
            <main>
                <h1>Main Content</h1>
                <p>This is the main content.</p>
            </main>
            <footer>Footer</footer>
        </body>
        </html>
        """

        content = converter.extract_main_content(html)
        soup = BeautifulSoup(content, "html.parser")

        # Should contain main content
        assert soup.find("h1") is not None
        assert "Main Content" in content

        # Should not contain navigation/footer
        assert "Navigation" not in content
        assert "Footer" not in content

    def test_extract_main_content_no_main_tag(self):
        """Test content extraction when no main tag exists."""
        converter = WorkatoDocsConverter()

        html = """
        <html>
        <body>
            <div class="content">
                <h1>Content Title</h1>
                <p>This is content without main tag.</p>
            </div>
        </body>
        </html>
        """

        content = converter.extract_main_content(html)
        soup = BeautifulSoup(content, "html.parser")

        # Should fallback to body content
        assert soup.find("h1") is not None
        assert "Content Title" in content

    def test_extract_main_content_with_sidebar(self):
        """Test content extraction removes sidebars."""
        converter = WorkatoDocsConverter()

        html = """
        <html>
        <body>
            <div class="sidebar">Navigation links</div>
            <main>
                <h1>Main Content</h1>
                <p>Content here.</p>
            </main>
            <div class="sidebar">More navigation</div>
        </body>
        </html>
        """

        content = converter.extract_main_content(html)
        assert "Navigation links" not in content
        assert "More navigation" not in content
        assert "Main Content" in content

    def test_post_process_markdown_basic(self):
        """Test markdown post-processing."""
        converter = WorkatoDocsConverter()

        markdown = """# Title

Some content with [links](https://example.com) and `code`.

## Section 2"""

        processed = converter.post_process_markdown(markdown, "https://example.com")

        # Should preserve structure
        assert "# Title" in processed
        assert "## Section 2" in processed
        assert "links" in processed
        assert "code" in processed

    def test_post_process_markdown_empty(self):
        """Test post-processing with empty input."""
        converter = WorkatoDocsConverter()
        result = converter.post_process_markdown("", "https://example.com")
        # Should add headers even for empty content
        assert "Workato SDK Documentation" in result
        assert "Source" in result

    def test_html_to_markdown_conversion(self):
        """Test full HTML to markdown conversion."""
        converter = WorkatoDocsConverter()

        html = """
        <html>
        <body>
            <main>
                <h1>Test Title</h1>
                <p>This is a paragraph with <strong>bold text</strong> and <em>italic text</em>.</p>
                <ul>
                    <li>List item 1</li>
                    <li>List item 2</li>
                </ul>
                <code>print("hello world")</code>
            </main>
        </body>
        </html>
        """

        result = converter.html_to_markdown(html, "https://example.com")

        # Should convert to markdown and add headers
        assert "Workato SDK Documentation" in result
        assert "# Test Title" in result
        assert "**bold text**" in result
        assert "_italic text_" in result  # html2text uses underscores for italics
        assert "* List item 1" in result
        assert "* List item 2" in result
        assert '`print("hello world")`' in result


class TestFetchPageContent:
    """Test the main page fetching function."""

    def test_fetch_page_content_success(self):
        """Test successful page fetching and conversion."""
        from unittest.mock import patch

        # Mock successful HTTP response
        mock_html = """
        <!DOCTYPE html>
        <html>
        <head><title>Test Page</title></head>
        <body>
            <header>Navigation</header>
            <main>
                <h1>Test Documentation</h1>
                <p>This is a comprehensive test page with sufficient content to pass validation.</p>
                <section>
                    <h2>Section 1</h2>
                    <p>This section contains detailed information about the topic being tested.</p>
                    <ul>
                        <li>Point one with detailed explanation</li>
                        <li>Point two with additional context</li>
                        <li>Point three with comprehensive details</li>
                    </ul>
                </section>
                <section>
                    <h2>Section 2</h2>
                    <p>This section provides additional context and examples to ensure the content
                    meets minimum length requirements for proper testing validation.</p>
                </section>
            </main>
            <footer>Footer content</footer>
        </body>
        </html>
        """

        with patch("requests.Session.get") as mock_get:
            mock_response = Mock()
            mock_response.text = mock_html
            mock_response.status_code = 200
            mock_response.headers = {"content-type": "text/html; charset=utf-8"}
            mock_response.raise_for_status = Mock()
            mock_get.return_value = mock_response

            converter = WorkatoDocsConverter()
            result = fetch_page_content(requests.Session(), converter, "https://example.com")

            assert result is not None
            assert result["url"] == "https://example.com"
            assert "content" in result
            assert "content_hash" in result

    @patch("scripts.fetch_workato_docs.requests.Session")
    def test_fetch_page_content_http_error(self, mock_session_class):
        """Test handling of HTTP errors."""
        # Mock HTTP error response
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.raise_for_status.side_effect = requests.HTTPError("404 Not Found")
        mock_session_class.return_value.get.return_value = mock_response

        converter = WorkatoDocsConverter()
        with pytest.raises(HTTPError):
            fetch_page_content(mock_session_class.return_value, converter, "https://example.com")

    @patch("scripts.fetch_workato_docs.requests.Session")
    def test_fetch_page_content_network_error(self, mock_session_class):
        """Test handling of network errors."""
        # Mock network error - these should be raised as NetworkError and retried
        mock_session_class.return_value.get.side_effect = requests.ConnectionError(
            "Connection failed"
        )

        converter = WorkatoDocsConverter()
        with pytest.raises(NetworkError):
            fetch_page_content(mock_session_class.return_value, converter, "https://example.com")

    @patch("scripts.fetch_workato_docs.requests.Session")
    def test_fetch_page_content_timeout(self, mock_session_class):
        """Test handling of timeouts."""
        # Mock timeout error - these should be raised as NetworkError and retried
        mock_session_class.return_value.get.side_effect = requests.Timeout("Request timed out")

        converter = WorkatoDocsConverter()
        with pytest.raises(NetworkError):
            fetch_page_content(mock_session_class.return_value, converter, "https://example.com")


class TestErrorConditions:
    """Test various error conditions and edge cases."""

    def test_url_to_filename_malformed_url(self):
        """Test URL parsing with malformed URLs."""
        # Missing protocol
        assert url_to_filename("docs.workato.com/test") == "docs.workato.com__test.md"

        # Invalid characters - spaces are preserved in filename
        url = "https://docs.workato.com/test file.html"
        result = url_to_filename(url)
        assert "test file" in result  # Spaces are preserved

    def test_converter_with_malformed_html(self):
        """Test converter with malformed HTML."""
        converter = WorkatoDocsConverter()

        # HTML with unclosed tags
        html = "<html><body><p>Unclosed paragraph<h1>Title</p>"
        result = converter.html_to_markdown(html, "https://example.com")

        # Should handle gracefully
        assert isinstance(result, str)
        assert len(result) > 0

    def test_converter_with_empty_html(self):
        """Test converter with empty HTML."""
        converter = WorkatoDocsConverter()
        result = converter.html_to_markdown("", "https://example.com")
        # Should add headers even for empty content
        assert "Workato SDK Documentation" in result
        assert "Source" in result

    def test_converter_with_binary_content(self):
        """Test converter with binary/non-text content."""
        converter = WorkatoDocsConverter()

        # Simulate binary content
        html = b"\x00\x01\x02\x03<html><body>Test</body></html>".decode("utf-8", errors="ignore")
        result = converter.html_to_markdown(html, "https://example.com")

        # Should handle gracefully
        assert isinstance(result, str)
