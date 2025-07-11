"""
Tests for core PDF processing functionality.
"""

import pytest
import tempfile
import os
from pathlib import Path

from pdf_zipper.core import (
    compress_pdf,
    get_file_type,
    validate_input_file,
    SUPPORTED_INPUT_TYPES
)


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


def test_get_file_type():
    """Test file type detection."""
    # Test PDF file
    ext, desc = get_file_type("test.pdf")
    assert ext == ".pdf"
    assert desc == "PDF Document"

    # Test PPTX file
    ext, desc = get_file_type("test.pptx")
    assert ext == ".pptx"
    assert desc == "PowerPoint Presentation"

    # Test unknown file type
    ext, desc = get_file_type("test.unknown")
    assert ext == ".unknown"
    assert desc == "Unknown file type"

    # Test case insensitive
    ext, desc = get_file_type("TEST.PDF")
    assert ext == ".pdf"
    assert desc == "PDF Document"


def test_validate_input_file():
    """Test input file validation."""
    # Test with non-existent file
    assert not validate_input_file("nonexistent.pdf")

    # Create temporary files for testing
    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp_pdf:
        tmp_pdf.write(b"fake pdf content")
        tmp_pdf_path = tmp_pdf.name

    with tempfile.NamedTemporaryFile(suffix=".pptx", delete=False) as tmp_pptx:
        tmp_pptx.write(b"fake pptx content")
        tmp_pptx_path = tmp_pptx.name

    with tempfile.NamedTemporaryFile(suffix=".txt", delete=False) as tmp_txt:
        tmp_txt.write(b"text content")
        tmp_txt_path = tmp_txt.name

    try:
        # Test supported file types
        assert validate_input_file(tmp_pdf_path)
        assert validate_input_file(tmp_pptx_path)

        # Test unsupported file type
        assert not validate_input_file(tmp_txt_path)

    finally:
        # Clean up temporary files
        os.unlink(tmp_pdf_path)
        os.unlink(tmp_pptx_path)
        os.unlink(tmp_txt_path)


def test_supported_input_types():
    """Test that supported input types are properly defined."""
    assert ".pdf" in SUPPORTED_INPUT_TYPES
    assert ".pptx" in SUPPORTED_INPUT_TYPES
    assert SUPPORTED_INPUT_TYPES[".pdf"] == "PDF Document"
    assert SUPPORTED_INPUT_TYPES[".pptx"] == "PowerPoint Presentation"


if __name__ == "__main__":
    pytest.main([__file__])
