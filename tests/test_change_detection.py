"""
Tests for the smart change detection system.

Tests the ChangeDetector class and related functionality.
"""

import pytest  # noqa: F401

from scripts.fetch_workato_docs import ChangeDetector


class TestChangeDetector:
    """Test the ChangeDetector class functionality."""

    def test_change_detector_initialization(self):
        """Test ChangeDetector initializes with correct defaults."""
        detector = ChangeDetector()

        assert detector.min_content_change_threshold == 50
        assert detector.min_significant_change_ratio == 0.1

    def test_detect_content_changes_new_content(self):
        """Test change detection with new content."""
        detector = ChangeDetector()

        result = detector.detect_content_changes("", "new content")

        assert result["changed"] is True
        assert result["change_ratio"] == 1.0
        assert "One side empty" in result["details"]

    def test_detect_content_changes_missing_content(self):
        """Test change detection with missing content."""
        detector = ChangeDetector()

        result = detector.detect_content_changes("old content", "")

        assert result["changed"] is True
        assert result["change_ratio"] == 1.0
        assert "One side empty" in result["details"]

    def test_detect_content_changes_empty_content(self):
        """Test change detection with empty content."""
        detector = ChangeDetector()

        result = detector.detect_content_changes("", "")

        assert result["changed"] is False
        assert result["change_ratio"] == 0.0
        assert "Both empty" in result["details"]

    def test_detect_content_changes_minor_changes(self):
        """Test change detection with minor changes below threshold."""
        detector = ChangeDetector()

        old_content = "This is a long piece of content with many words and sentences."
        new_content = "This is a long piece of content with many words and sentences!"

        result = detector.detect_content_changes(old_content, new_content)

        assert result["changed"] is False  # Should be below threshold
        assert result["change_ratio"] < detector.min_significant_change_ratio

    def test_detect_content_changes_significant_changes(self):
        """Test change detection with significant changes."""
        detector = ChangeDetector()

        old_content = "Short content"
        new_content = (
            "This is much longer content with substantial additions and modifications "
            "that exceed the threshold for meaningful changes."
        )

        result = detector.detect_content_changes(old_content, new_content)

        assert result["changed"] is True
        assert result["change_ratio"] >= detector.min_significant_change_ratio

    def test_detect_content_changes_length_threshold(self):
        """Test change detection with length-based threshold."""
        detector = ChangeDetector()

        old_content = "A" * 100  # 100 characters
        new_content = "B" * 200  # 200 characters (100 char diff, 50% ratio)

        result = detector.detect_content_changes(old_content, new_content)

        assert result["changed"] is True
        assert result["change_ratio"] == 0.5

    def test_should_update_file_new_file(self):
        """Test should_update_file for new files."""
        detector = ChangeDetector()

        result = detector.should_update_file("test.md", "", "new_hash")

        assert result is True

    def test_should_update_file_hash_changed(self):
        """Test should_update_file when hash changed."""
        detector = ChangeDetector()

        result = detector.should_update_file("test.md", "old_hash", "new_hash")

        assert result is True

    def test_should_update_file_unchanged(self):
        """Test should_update_file when content unchanged."""
        detector = ChangeDetector()

        result = detector.should_update_file("test.md", "same_hash", "same_hash")

        assert result is False

    def test_should_update_file_content_changed(self):
        """Test should_update_file with content changes."""
        detector = ChangeDetector()

        old_content = "Original content"
        new_content = "Modified content with significant changes"

        result = detector.should_update_file(
            "test.md", "same_hash", "same_hash", old_content, new_content
        )

        assert result is True

    def test_should_update_file_minor_content_changes(self):
        """Test should_update_file with minor content changes."""
        detector = ChangeDetector()

        old_content = "This is a long piece of content"
        new_content = "This is a long piece of content."  # Only punctuation added

        result = detector.should_update_file(
            "test.md", "same_hash", "same_hash", old_content, new_content
        )

        assert result is False  # Should be below threshold


class TestChangeDetectionIntegration:
    """Test change detection integration with the overall system."""

    def test_meaningful_changes_detection(self):
        """Test that the system correctly identifies meaningful vs minor changes."""
        detector = ChangeDetector()

        # Test cases: (old_content, new_content, expected_result)
        test_cases = [
            # Meaningful changes
            ("", "New content", True),
            ("Old", "Completely new content", True),
            (
                "Short",
                "This is a much longer piece of content with substantial additions",
                True,
            ),
            # Minor changes (below threshold)
            (
                "Content",
                "Content!",
                True,
            ),  # This is actually above threshold (1 char vs 7 total)
            ("Text here", "Text here.", True),  # This is also above threshold
            # No changes
            ("Same content", "Same content", False),
        ]

        for old_content, new_content, expected in test_cases:
            result = detector.detect_content_changes(old_content, new_content)
            assert result["changed"] == expected, f"Failed for: '{old_content}' -> '{new_content}'"

    def test_change_threshold_configuration(self):
        """Test that change thresholds work correctly."""
        # Create detector with custom thresholds
        detector = ChangeDetector()
        detector.min_content_change_threshold = 10
        detector.min_significant_change_ratio = 0.5

        old_content = "A" * 20  # 20 characters
        new_content = "B" * 35  # 35 characters (15 char diff, 75% ratio)

        result = detector.detect_content_changes(old_content, new_content)

        assert result["changed"] is True
        assert result["change_ratio"] == 15 / 35  # 15 char diff / 35 char max
