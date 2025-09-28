"""
Integration tests for the documentation fetching pipeline.

Tests the end-to-end process of fetching and processing Workato documentation.
"""

import tempfile
from pathlib import Path
from unittest.mock import Mock, patch

import pytest
import requests

from scripts.fetch_workato_docs import (
    HTTPError,
    NetworkError,
    WorkatoDocsConverter,
    fetch_page_content,
    load_manifest,
    save_manifest,
    url_to_filename,
)


class TestEndToEndFetching:
    """Test complete documentation fetching workflows."""

    def test_fetch_single_page_success(self):
        """Test fetching a single page end-to-end."""
        # Mock successful HTTP response
        mock_html = """
        <!DOCTYPE html>
        <html>
        <body>
            <main>
                <h1>Test Documentation</h1>
                <p>This is test content for integration testing.</p>
                <section>
                    <h2>Section 1</h2>
                    <p>Some content here.</p>
                </section>
            </main>
        </body>
        </html>
        """

        with patch("requests.Session.get") as mock_get:
            mock_response = Mock()
            mock_response.text = mock_html
            mock_response.status_code = 200
            mock_response.headers = {"content-type": "text/html; charset=utf-8"}
            mock_get.return_value = mock_response

            converter = WorkatoDocsConverter()
            result = fetch_page_content(
                requests.Session(),
                converter,
                "https://docs.workato.com/en/developing-connectors/sdk/test.html",
            )

            assert result is not None
            assert (
                result["url"] == "https://docs.workato.com/en/developing-connectors/sdk/test.html"
            )
            assert "content" in result
            assert "content_hash" in result

            # Verify content was converted
            assert "Test Documentation" in result["content"]
            assert "Section 1" in result["content"]

    def test_fetch_page_with_network_error(self):
        """Test handling of network errors during fetching."""
        converter = WorkatoDocsConverter()

        with patch("requests.Session.get") as mock_get:
            mock_get.side_effect = requests.ConnectionError("Network unreachable")

            with pytest.raises(NetworkError):
                fetch_page_content(
                    requests.Session(),
                    converter,
                    "https://docs.workato.com/en/developing-connectors/sdk/test.html",
                )

    def test_fetch_page_with_http_error(self):
        """Test handling of HTTP errors during fetching."""
        with patch("scripts.fetch_workato_docs.requests.Session.get") as mock_get:
            mock_response = Mock()
            mock_response.status_code = 404
            mock_response.raise_for_status.side_effect = requests.HTTPError("404 Not Found")
            mock_get.return_value = mock_response

        converter = WorkatoDocsConverter()
        with pytest.raises(HTTPError):
            fetch_page_content(
                requests.Session(),
                converter,
                "https://docs.workato.com/en/developing-connectors/sdk/test.html",
            )

    def test_manifest_integration(self):
        """Test manifest loading, updating, and saving."""
        with tempfile.TemporaryDirectory() as tmpdir:
            manifest_path = Path(tmpdir) / "manifest.json"

            # Start with empty manifest
            manifest = load_manifest(manifest_path)
            assert manifest["files"] == {}

            # Add a file entry
            test_file = "test.md"
            test_data = {
                "original_url": "https://example.com/test.html",
                "hash": "abc123",
                "last_updated": "2023-01-01T00:00:00",
            }

            manifest["files"][test_file] = test_data
            save_manifest(manifest_path.parent, manifest)

            # Verify it was saved and can be loaded
            loaded = load_manifest(manifest_path.parent)
            assert test_file in loaded["files"]
            assert loaded["files"][test_file]["hash"] == "abc123"

    def test_url_to_filename_integration(self):
        """Test URL to filename conversion with various SDK URLs."""
        test_cases = [
            (
                "https://docs.workato.com/en/developing-connectors/sdk/cli.html",
                "cli.md",
            ),
            (
                "https://docs.workato.com/en/developing-connectors/sdk/guides/authentication.html",
                "guides__authentication.md",
            ),
            (
                "https://docs.workato.com/en/developing-connectors/sdk/sdk-reference/actions.html",
                "sdk-reference__actions.md",
            ),
        ]

        for url, expected in test_cases:
            result = url_to_filename(url)
            assert result == expected, f"URL {url} -> {result}, expected {expected}"


class TestErrorRecovery:
    """Test error recovery and resilience."""

    def test_partial_failure_recovery(self):
        """Test that one failed page doesn't break the entire batch."""
        # This would be tested in a batch processing scenario
        # where multiple URLs are processed and some fail
        pass

    def test_corrupted_manifest_recovery(self):
        """Test recovery from corrupted manifest files."""
        with tempfile.TemporaryDirectory() as tmpdir:
            manifest_path = Path(tmpdir) / "manifest.json"

            # Write corrupted JSON
            manifest_path.write_text("invalid json content {")

            # Should handle gracefully and return empty manifest
            manifest = load_manifest(manifest_path)
            assert manifest == {"files": {}, "last_updated": None}

    def test_disk_space_error_handling(self):
        """Test handling of disk space errors during saving."""
        # This would mock file system errors during write operations
        pass


class TestContentValidation:
    """Test that fetched content meets quality standards."""

    def test_minimum_content_length(self):
        """Test that fetched content has minimum required length."""
        mock_html = """
        <!DOCTYPE html>
        <html>
        <head><title>Test Page</title></head>
        <body>
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
        </body>
        </html>
        """

        with patch("requests.Session.get") as mock_get:
            mock_response = Mock()
            mock_response.text = mock_html
            mock_response.status_code = 200
            mock_response.headers = {"content-type": "text/html; charset=utf-8"}
            mock_get.return_value = mock_response

            converter = WorkatoDocsConverter()
            result = fetch_page_content(
                requests.Session(),
                converter,
                "https://docs.workato.com/en/developing-connectors/sdk/test.html",
            )

            assert result is not None
            # Content should be substantial
            assert len(result["content"]) > 50

    def test_content_has_required_sections(self):
        """Test that content contains expected sections."""
        mock_html = """
        <html>
        <body>
            <main>
                <h1>Test Page</h1>
                <p>Introduction paragraph.</p>
                <h2>Configuration</h2>
                <p>Configuration details.</p>
            </main>
        </body>
        </html>
        """

        with patch("requests.Session.get") as mock_get:
            mock_response = Mock()
            mock_response.text = mock_html
            mock_response.status_code = 200
            mock_response.headers = {"content-type": "text/html; charset=utf-8"}
            mock_get.return_value = mock_response

            converter = WorkatoDocsConverter()
            result = fetch_page_content(
                requests.Session(),
                converter,
                "https://docs.workato.com/en/developing-connectors/sdk/test.html",
            )

            content = result["content"]
            assert "Test Page" in content
            assert "Configuration" in content
            assert "Introduction paragraph" in content
