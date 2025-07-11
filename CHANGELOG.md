# Changelog

All notable changes to PDF Zipper will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.1] - 2025-01-10

### Removed
- **Pandoc Support**: Removed Pandoc from PPTX conversion tools as it doesn't support PPTX to PDF conversion
- **Unnecessary Dependencies**: Cleaned up conversion tool detection

### Improved
- **GUI Enhancement**: Added comprehensive tool status display in GUI
- **System Information**: New "System Info" tab showing available conversion tools
- **User Experience**: Better error messages and installation guidance
- **Tool Detection**: More accurate detection of available conversion tools

### Added
- **Enhanced GUI**: Tool status indicators in PPTX to PDF tab
- **System Info Tab**: Real-time display of system and tool information
- **Refresh Functionality**: Button to refresh tool status in GUI
- **Better Logging**: Detailed tool availability information in GUI logs

### Technical Details
- Focused on LibreOffice and unoconv as primary conversion tools
- Improved fallback method with better user guidance
- Enhanced GUI with real-time tool status monitoring
- Cleaner codebase with removed unused Pandoc integration

## [1.1.0] - 2025-01-10

### Added
- **PPTX to PDF Conversion**: New feature to convert PowerPoint presentations to PDF format
- **Multi-format Input Support**: Both CLI and GUI now accept PDF and PPTX files as input
- **Bi-directional Conversion**: Convert between PDF and PowerPoint formats (PDF ↔ PPTX)
- **Enhanced File Type Detection**: Automatic file type validation and format detection
- **Cross-platform PPTX Conversion**: Support for Windows COM interface and cross-platform methods
- **New CLI Commands**: Extended `compress` and `convert` commands to handle PPTX files
- **Enhanced GUI**: Added "PPTX to PDF" tab and improved file selection logic
- **Comprehensive Testing**: Added unit tests for new file type detection and validation features

### Changed
- **CLI Interface**: `compress` command now supports PPTX input files (converts to PDF)
- **CLI Interface**: `convert` command now supports bi-directional conversion
- **CLI Interface**: `info` command now displays information for both PDF and PPTX files
- **GUI Interface**: File selection now supports multiple formats with clear type indicators
- **Documentation**: Updated README with new features and usage examples
- **Dependencies**: Added Windows-specific dependencies for better PPTX conversion support

### Improved
- **Error Handling**: Better error messages for unsupported file types
- **User Experience**: Clear file type indicators in GUI and CLI
- **Performance**: Optimized file type detection and validation
- **Compatibility**: Enhanced cross-platform support for PPTX processing

### Technical Details
- Added `convert_pptx_to_pdf()` function with Windows COM and cross-platform fallback
- Added `get_file_type()` and `validate_input_file()` utility functions
- Extended `SUPPORTED_INPUT_TYPES` and `SUPPORTED_OUTPUT_TYPES` constants
- Updated all CLI commands to handle multiple input formats
- Enhanced GUI with new tab and improved file handling logic

## [1.0.0] - 2025-01-10

### Added
- **Initial Release**: PDF compression and PDF to PowerPoint conversion
- **GUI Interface**: Beautiful terminal-based interface using Textual
- **CLI Interface**: Comprehensive command-line interface with rich output
- **Auto Compression**: Automatically compress PDFs to target file sizes
- **Manual Compression**: Compress PDFs with custom DPI settings
- **PDF to PowerPoint**: Convert PDF pages to PowerPoint slides
- **Drag & Drop Support**: Easy file selection in GUI mode
- **Cross-platform Support**: Works on macOS, Linux, and Windows
- **PyPI Distribution**: Available via `pip install pdf-zipper`
- **Standalone Executables**: Pre-built executables for major platforms

### Features
- Smart PDF compression with automatic optimization
- PDF to PowerPoint conversion with customizable DPI
- Modern terminal-based GUI with file tree navigation
- Rich CLI output with progress indicators
- Comprehensive logging and error handling
- Easy installation and distribution
