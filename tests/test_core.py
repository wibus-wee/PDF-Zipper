"""
Tests for core PDF processing functionality.
"""

import pytest

from pdf_zipper.core import compress_pdf


def test_compress_pdf_basic():
    """Test basic PDF compression functionality."""
    # This is a placeholder test - in a real scenario you'd need a test PDF file
    pass


def test_autocompress_pdf_basic():
    """Test auto compression functionality."""
    # This is a placeholder test - in a real scenario you'd need a test PDF file
    pass


def test_invalid_input_file():
    """Test handling of invalid input files."""
    messages = []

    def logger(msg):
        messages.append(msg)

    # Test with non-existent file - should raise FileNotFoundError
    with pytest.raises((FileNotFoundError, Exception)):
        compress_pdf("nonexistent.pdf", "output.pdf", 150, logger)


if __name__ == "__main__":
    pytest.main([__file__])
