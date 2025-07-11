# Changelog

All notable changes to PDF Zipper will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.2.2] - 2025-01-11

### Fixed
- **🎨 GUI Log Color Rendering**: Fixed Rich markup rendering in GUI log output - colors and formatting now display correctly instead of showing raw markup syntax
- **🔄 File Tree Refresh**: Added file tree refresh functionality with F5 keyboard shortcut to update file list when filesystem changes
- **🖥️ GUI Layout Stability**: Improved GUI layout consistency and removed layout disruption issues

### Enhanced
- **⌨️ Keyboard Shortcuts**: Added F5 key binding for refreshing file tree in GUI
- **📝 Log Display**: Enhanced log readability with proper Rich markup parsing (emojis, colors, formatting)
- **🔧 User Experience**: Improved overall GUI responsiveness and visual feedback

### Technical Details
- **RichLog Configuration**: Added `markup=True` parameter to enable Rich markup parsing in Textual RichLog component
- **Action Binding**: Implemented `action_refresh_tree()` method with DirectoryTree reload functionality
- **Layout Optimization**: Simplified GUI layout structure for better stability and performance

## [1.2.1] - 2025-01-11

### Fixed
- **🎯 Critical Fix: PDF→PPTX Target Size Calculation**: Fixed DPI optimization to base calculations on final PPTX file size instead of intermediate PDF size
- **📊 Accurate Size Control**: PDF to PPTX conversion now correctly achieves user-specified target file sizes
- **🔧 Image Compression Optimization**: Improved PDF to PPTX conversion with JPEG compression and intelligent quality adjustment based on document size
- **💾 Memory Management**: Enhanced temporary file handling during cross-format conversions

### Technical Details
- **Root Cause**: Previous logic optimized DPI based on PDF size, then converted to PPTX, causing target size inaccuracy
- **Solution**: New `_find_optimal_dpi_for_pptx()` function performs DPI optimization directly on PPTX output
- **Process**: Each iteration now generates PDF → converts to PPTX → checks PPTX size → adjusts DPI accordingly
- **Impact**: All interfaces (CLI, GUI, API) now provide accurate target size control for PDF→PPTX conversions

## [1.2.0] - 2025-01-11

### Added
- **🎯 PPTX Auto Compression**: New feature to automatically compress PPTX files to target file size
- **Universal Auto Compression**: New `autocompress()` function that supports both PDF and PPTX files
- **Enhanced CLI**: CLI now supports PPTX auto compression with `--target-size` parameter
- **Enhanced GUI**: GUI auto compression now works with both PDF and PPTX files
- **New API Functions**: Added `autocompress_pptx()` for PPTX-specific compression

### Improved
- **Code Architecture**: Refactored DPI optimization logic into reusable `_find_optimal_dpi()` function
- **File Format Preservation**: Auto compression now maintains original file format (PPTX → PPTX, PDF → PDF)
- **Error Handling**: Enhanced error handling and temporary file management for PPTX processing
- **Documentation**: Updated README with comprehensive examples and usage instructions

### Technical Details
- **PPTX Compression Workflow**: PPTX → PDF → DPI optimization → PPTX conversion chain
- **Binary Search Algorithm**: Uses iterative DPI optimization to achieve precise target file sizes
- **Backward Compatibility**: All existing APIs remain unchanged and fully functional
- **Temporary File Management**: Automatic cleanup of intermediate files during PPTX processing

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
