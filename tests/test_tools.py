import os
import sys
from datetime import datetime
from typing import Any
from unittest.mock import patch

import pytest

# Import implementation based on file path.
# We add the parent directory to sys.path to ensure 'tools' is importable.
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from tools import save_to_txt


def test_save_to_txt_success(tmp_path: Any) -> None:
    """Test saving research data to a specific file with successful response."""
    test_data = "Detailed research findings about the moon."
    test_file = tmp_path / "moon_research.txt"
    test_filename = str(test_file)
    fixed_now = datetime(2026, 2, 19, 10, 30, 0)

    # Mocking datetime in the tools module to have a predictable timestamp
    with patch("tools.datetime") as mock_datetime:
        mock_datetime.now.return_value = fixed_now

        # Execute the tool via its run method. Since it's a multi-argument tool, 
        # we pass a dictionary of arguments.
        result = save_to_txt.run({"data": test_data, "filename": test_filename})

        # When comparing, provide the expected value as the first argument
        expected_msg = f"Data successfully saved to {test_filename}"
        assert expected_msg == result

        # Verify file creation and content
        assert os.path.exists(test_filename)
        with open(test_filename, "r", encoding="utf-8") as f:
            content = f.read()

        timestamp_str = fixed_now.strftime("%Y-%m-%d_%H:%M:%S")
        expected_content = (
            f"--- Research Output ---\n"
            f"Timestamp: {timestamp_str}\n\n"
            f"{test_data}\n\n"
        )
        assert expected_content == content


def test_save_to_txt_append_content(tmp_path: Any) -> None:
    """Test that save_to_txt appends content to an existing file."""
    test_file = tmp_path / "append_test.txt"
    test_filename = str(test_file)

    initial_text = "Initial content.\n"
    with open(test_filename, "w", encoding="utf-8") as f:
        f.write(initial_text)

    new_data = "New research data."
    fixed_now = datetime(2026, 2, 19, 11, 0, 0)

    with patch("tools.datetime") as mock_datetime:
        mock_datetime.now.return_value = fixed_now

        save_to_txt.run({"data": new_data, "filename": test_filename})

        with open(test_filename, "r", encoding="utf-8") as f:
            content = f.read()

        timestamp_str = fixed_now.strftime("%Y-%m-%d_%H:%M:%S")
        expected_added_content = (
            f"--- Research Output ---\n"
            f"Timestamp: {timestamp_str}\n\n"
            f"{new_data}\n\n"
        )
        # Expected value first
        assert (initial_text + expected_added_content) == content


def test_save_to_txt_default_filename(tmp_path: Any, monkeypatch: pytest.MonkeyPatch) -> None:
    """Test saving research data using the default filename."""
    # Use monkeypatch to change the current working directory to tmp_path
    monkeypatch.chdir(tmp_path)

    test_data = "Default file content."
    default_filename = "research_output.txt"
    fixed_now = datetime(2026, 2, 19, 12, 0, 0)

    with patch("tools.datetime") as mock_datetime:
        mock_datetime.now.return_value = fixed_now

        result = save_to_txt.run({"data": test_data})

        # Expected value first
        expected_msg = f"Data successfully saved to {default_filename}"
        assert expected_msg == result
        assert os.path.exists(default_filename)

        with open(default_filename, "r", encoding="utf-8") as f:
            content = f.read()

        timestamp_str = fixed_now.strftime("%Y-%m-%d_%H:%M:%S")
        expected_content = (
            f"--- Research Output ---\n"
            f"Timestamp: {timestamp_str}\n\n"
            f"{test_data}\n\n"
        )
        assert expected_content == content


if __name__ == "__main__":
    # Make the test file executable directly
    pytest.main([__file__])
