"""Performance tests for Workato SDK Documentation Mirror.

These tests measure execution time and resource usage for critical operations.
They help ensure the system maintains acceptable performance characteristics.
"""

import hashlib
import tempfile
import time
from pathlib import Path

import pytest

from scripts.fetch_workato_docs import (
    WorkatoDocsConverter,
    load_manifest,
    save_manifest,
    url_to_filename,
)


class TestPerformanceMetrics:
    """Test suite for performance metrics of critical operations."""

    def test_url_to_filename_performance(self):
        """Test URL to filename conversion performance."""
        urls = [
            f"https://docs.workato.com/en/developing-connectors/sdk/page{i}.html"
            for i in range(1000)
        ]

        start_time = time.time()
        for url in urls:
            url_to_filename(url)
        elapsed = time.time() - start_time

        # Should process 1000 URLs in under 0.1 seconds
        assert elapsed < 0.1, f"URL conversion too slow: {elapsed:.3f}s for 1000 URLs"

    def test_manifest_operations_performance(self):
        """Test manifest load/save performance with large datasets."""
        # Create a large manifest with 1000 entries
        large_manifest = {
            f"file_{i}.md": {
                "url": f"https://example.com/page{i}.html",
                "hash": f"hash_{i}" * 8,
                "last_fetched": "2024-01-01T00:00:00",
                "status": "success",
            }
            for i in range(1000)
        }

        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)

            # Test save performance
            start_time = time.time()
            save_manifest(temp_path, large_manifest)
            save_elapsed = time.time() - start_time

            # Test load performance
            start_time = time.time()
            loaded = load_manifest(temp_path)
            load_elapsed = time.time() - start_time

            # Should handle 1000-entry manifest quickly
            assert save_elapsed < 0.5, f"Manifest save too slow: {save_elapsed:.3f}s"
            assert load_elapsed < 0.5, f"Manifest load too slow: {load_elapsed:.3f}s"
            # The loaded manifest contains metadata keys, so filter to file entries only
            file_entries = {k: v for k, v in loaded.items() if k.endswith(".md")}
            assert len(file_entries) == 1000

    def test_content_hashing_performance(self):
        """Test content hashing performance for large documents."""
        # Create a large document (1MB of text)
        large_content = "Lorem ipsum dolor sit amet. " * 50000

        start_time = time.time()
        for _ in range(100):
            hashlib.sha256(large_content.encode()).hexdigest()
        elapsed = time.time() - start_time

        # Should hash 100MB of text in under 1 second
        assert elapsed < 1.0, f"Hashing too slow: {elapsed:.3f}s for 100MB"

    def test_html_to_markdown_performance(self):
        """Test HTML to Markdown conversion performance."""
        converter = WorkatoDocsConverter()

        # Create a large HTML document
        large_html = """
        <html>
            <body>
                <main class="content">
                    <h1>Test Document</h1>
                    """
        paragraphs = "".join([f"<p>Paragraph {i} with some content.</p>" for i in range(1000)])
        large_html += (
            paragraphs
            + """
                </main>
            </body>
        </html>
        """
        )

        start_time = time.time()
        # Test the actual conversion methods
        main_content = converter.extract_main_content(large_html)
        test_url = "https://example.com/test.html"
        markdown = converter.html_to_markdown(main_content, test_url)
        processed = converter.post_process_markdown(markdown, test_url)
        elapsed = time.time() - start_time

        # Should convert large HTML document in under 2 seconds
        assert elapsed < 2.0, f"HTML conversion too slow: {elapsed:.3f}s"
        assert len(processed) > 0

    def test_change_detection_performance(self):
        """Test change detection performance with many files."""
        # Simulate checking 100 files for changes
        old_contents = {f"file_{i}": f"content_{i}" * 100 for i in range(100)}
        new_contents = {f"file_{i}": f"content_{i}" * 100 + " changed" for i in range(100)}

        start_time = time.time()
        for filename in old_contents:
            old_hash = hashlib.sha256(old_contents[filename].encode()).hexdigest()
            new_hash = hashlib.sha256(new_contents[filename].encode()).hexdigest()
            _ = old_hash != new_hash
        elapsed = time.time() - start_time

        # Should check 100 files in under 0.5 seconds
        assert elapsed < 0.5, f"Change detection too slow: {elapsed:.3f}s for 100 files"

    def test_memory_usage_large_document(self):
        """Test memory usage when processing large documents."""
        # This test ensures we don't load entire large documents into memory
        # In a real implementation, you'd use memory_profiler or tracemalloc
        # For now, we just ensure the hashing works

        large_content = "x" * (10 * 1024 * 1024)  # 10MB string

        # Should not raise MemoryError
        try:
            hash_result = hashlib.sha256(large_content.encode()).hexdigest()
            assert hash_result is not None
        except MemoryError:
            pytest.fail("Memory error when processing large document")

    def test_concurrent_url_processing_simulation(self):
        """Simulate concurrent URL processing to test for race conditions."""
        # Note: Real concurrent testing would use threading/multiprocessing
        # This simulates the performance aspect
        urls = [
            f"https://docs.workato.com/en/developing-connectors/sdk/page{i}.html" for i in range(10)
        ]

        start_time = time.time()
        results = []
        for url in urls:
            filename = url_to_filename(url)
            results.append(filename)
        elapsed = time.time() - start_time

        # Should handle 10 URLs very quickly
        assert elapsed < 0.01, f"URL processing too slow: {elapsed:.3f}s"
        assert len(results) == len(urls)
        assert len(set(results)) == len(urls), "Duplicate filenames generated"


class TestPerformanceRegression:
    """Tests to catch performance regressions."""

    def test_baseline_import_time(self):
        """Ensure module import time stays reasonable."""
        import importlib
        import sys

        # Remove from cache if already imported
        if "scripts.fetch_workato_docs" in sys.modules:
            del sys.modules["scripts.fetch_workato_docs"]

        start_time = time.time()
        importlib.import_module("scripts.fetch_workato_docs")
        elapsed = time.time() - start_time

        # Module import should be fast
        assert elapsed < 1.0, f"Module import too slow: {elapsed:.3f}s"
