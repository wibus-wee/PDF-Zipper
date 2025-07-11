"""
PDF Zipper - A powerful file processing tool with GUI and CLI interfaces.

This package provides both command-line and graphical user interfaces
for compressing PDF files, converting between PDF and PowerPoint formats,
and performing various file processing tasks with multi-format support.
"""

__version__ = "1.2.2"
__author__ = "wibus-wee"
__email__ = "wibus_wee@outlook.com"

from .core import (
    autocompress,
    autocompress_pdf,
    autocompress_pdf_to_pptx,
    autocompress_pptx,
    compress_pdf,
    convert_to_ppt,
    convert_pptx_to_pdf,
    get_file_type,
    validate_input_file,
    SUPPORTED_INPUT_TYPES,
    SUPPORTED_OUTPUT_TYPES
)

__all__ = [
    "autocompress",
    "autocompress_pdf",
    "autocompress_pdf_to_pptx",
    "autocompress_pptx",
    "compress_pdf",
    "convert_to_ppt",
    "convert_pptx_to_pdf",
    "get_file_type",
    "validate_input_file",
    "SUPPORTED_INPUT_TYPES",
    "SUPPORTED_OUTPUT_TYPES",
    "__version__",
]
