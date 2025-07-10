"""
PDF Zipper - A powerful PDF compression tool with GUI and CLI interfaces.

This package provides both command-line and graphical user interfaces
for compressing PDF files, converting them to PowerPoint presentations,
and performing various PDF optimization tasks.
"""

__version__ = "1.0.0"
__author__ = "PDF Zipper Team"
__email__ = "team@pdfzipper.com"

from .core import autocompress_pdf, compress_pdf, convert_to_ppt

__all__ = [
    "autocompress_pdf",
    "compress_pdf",
    "convert_to_ppt",
    "__version__",
]
