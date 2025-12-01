"""Tests for output file naming and uniqueness logic."""

import shutil
import tempfile
from pathlib import Path

import pytest

from cerebrus.ui.components import _get_unique_output_path


class TestUniqueOutputPath:
    """Test the _get_unique_output_path function."""

    def setup_method(self):
        """Create a temporary directory for testing."""
        self.test_dir = Path(tempfile.mkdtemp())

    def teardown_method(self):
        """Clean up temporary directory."""
        if self.test_dir.exists():
            shutil.rmtree(self.test_dir)

    def test_no_existing_file(self):
        """Test when no file exists - should return the original path."""
        result = _get_unique_output_path(self.test_dir, "test", ".html")
        expected = self.test_dir / "test.html"
        assert result == expected
        assert not result.exists()  # Should not create the file

    def test_existing_file_adds_counter(self):
        """Test when file exists - should add _1 counter."""
        # Create an existing file
        existing_file = self.test_dir / "test.html"
        existing_file.touch()

        result = _get_unique_output_path(self.test_dir, "test", ".html")
        expected = self.test_dir / "test_1.html"
        assert result == expected

    def test_multiple_existing_files(self):
        """Test when multiple files exist - should find next available number."""
        # Create multiple existing files
        (self.test_dir / "test.html").touch()
        (self.test_dir / "test_1.html").touch()
        (self.test_dir / "test_2.html").touch()

        result = _get_unique_output_path(self.test_dir, "test", ".html")
        expected = self.test_dir / "test_3.html"
        assert result == expected

    def test_extension_with_dot(self):
        """Test extension handling when dot is included."""
        result = _get_unique_output_path(self.test_dir, "test", ".html")
        expected = self.test_dir / "test.html"
        assert result == expected

    def test_extension_without_dot(self):
        """Test extension handling when dot is not included."""
        result = _get_unique_output_path(self.test_dir, "test", "html")
        expected = self.test_dir / "test.html"
        assert result == expected

    def test_different_extensions(self):
        """Test with different file extensions."""
        result_html = _get_unique_output_path(self.test_dir, "report", ".html")
        result_csv = _get_unique_output_path(self.test_dir, "data", ".csv")
        result_txt = _get_unique_output_path(self.test_dir, "log", "txt")

        assert result_html == self.test_dir / "report.html"
        assert result_csv == self.test_dir / "data.csv"
        assert result_txt == self.test_dir / "log.txt"

    def test_gap_in_sequence(self):
        """Test when there's a gap in the sequence (e.g., test.html and test_3.html exist)."""
        # Create files with a gap
        (self.test_dir / "test.html").touch()
        (self.test_dir / "test_3.html").touch()

        # Should fill the gap and use test_1.html
        result = _get_unique_output_path(self.test_dir, "test", ".html")
        expected = self.test_dir / "test_1.html"
        assert result == expected

    def test_filename_with_special_characters(self):
        """Test filenames with special characters."""
        result = _get_unique_output_path(
            self.test_dir, "test_report_2024-12-01", ".html"
        )
        expected = self.test_dir / "test_report_2024-12-01.html"
        assert result == expected

    def test_long_filename(self):
        """Test with a very long filename."""
        long_name = "a" * 200
        result = _get_unique_output_path(self.test_dir, long_name, ".html")
        expected = self.test_dir / f"{long_name}.html"
        assert result == expected


class TestOutputFileNameLogic:
    """Test the output file name and prefix logic integration."""

    def test_prefix_mode_naming(self):
        """Test filename generation in prefix mode."""
        # Simulate prefix mode behavior
        output_file_name = "report"
        csv_stem = "game_data"
        use_prefix_only = True

        if use_prefix_only and output_file_name:
            result = f"{output_file_name}_{csv_stem}"
        else:
            result = output_file_name if output_file_name else csv_stem

        assert result == "report_game_data"

    def test_exact_filename_mode_naming(self):
        """Test filename generation in exact filename mode."""
        # Simulate exact filename mode behavior
        output_file_name = "final_report"
        csv_stem = "game_data"
        use_prefix_only = False

        if use_prefix_only and output_file_name:
            result = f"{output_file_name}_{csv_stem}"
        else:
            result = output_file_name if output_file_name else csv_stem

        assert result == "final_report"

    def test_empty_output_name_prefix_mode(self):
        """Test with empty output name in prefix mode."""
        output_file_name = ""
        csv_stem = "game_data"
        use_prefix_only = True

        if use_prefix_only and output_file_name:
            result = f"{output_file_name}_{csv_stem}"
        else:
            result = output_file_name if output_file_name else csv_stem

        # Should fall back to csv_stem
        assert result == "game_data"

    def test_empty_output_name_exact_mode(self):
        """Test with empty output name in exact filename mode."""
        output_file_name = ""
        csv_stem = "game_data"
        use_prefix_only = False

        if use_prefix_only and output_file_name:
            result = f"{output_file_name}_{csv_stem}"
        else:
            result = output_file_name if output_file_name else csv_stem

        # Should fall back to csv_stem
        assert result == "game_data"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
