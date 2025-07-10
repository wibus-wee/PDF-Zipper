# 🗜️ PDF Zipper

<div align="center">

[![PyPI version](https://badge.fury.io/py/pdf-zipper.svg)](https://badge.fury.io/py/pdf-zipper)
![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Platform](https://img.shields.io/badge/platform-macOS%20%7C%20Linux%20-lightgrey.svg)
![Status](https://img.shields.io/badge/status-stable-brightgreen.svg)

</div>

A powerful PDF compression tool with both GUI and CLI interfaces, built with modern Python.

## 📸 Screenshots

<div align="center">
<table>
<tr>
<td width="50%">

### 🖥️ Beautiful Terminal GUI
![GUI Interface](./examples/screenshot-gui.png)
*Interactive file browser with drag & drop support*

</td>
<td width="50%">

### ⌨️ Powerful Command Line Interface
![CLI Interface](./examples/screenshot-cli.png)
*Rich output with progress indicators and detailed info*

</td>
</tr>
</table>
</div>

## ✨ Features

- **🎯 Auto Compression**: Automatically compress PDFs to a target file size
- **🔧 Manual Compression**: Compress PDFs with custom DPI settings  
- **📊 PDF to PowerPoint**: Convert PDF pages to PowerPoint slides
- **🖥️ Beautiful GUI**: Modern terminal-based interface using Textual
- **⌨️ CLI Interface**: Full command-line support with rich output
- **📁 Drag & Drop Support**: Easy file selection in GUI mode
- **📦 Easy Installation**: Install as a system command

## 🚀 Installation

### From PyPI (Recommended)
```bash
pip install pdf-zipper
```

### From Source
```bash
git clone https://github.com/your-username/pdf-zipper.git
cd pdf-zipper
pip install -e .
```

### Standalone Executable (No Python Required)

Download the pre-built executable for your platform:

**macOS (Apple Silicon)**
```bash
# Option 1: App Bundle (Recommended for GUI users)
# Download PDF-Zipper-darwin-arm64.app from releases page
# Double-click to launch GUI interface

# Option 2: Command Line Executable
# Download from releases page
chmod +x pdf-zipper-gui-darwin-arm64
./pdf-zipper-gui-darwin-arm64 --help
./pdf-zipper-gui-darwin-arm64 gui  # Launch GUI
```

**Windows**
```cmd
REM Download from releases page
pdf-zipper-cli-windows-x64.exe --help
```

**Linux**
```bash
# Download from releases page
chmod +x pdf-zipper-cli-linux-x64
./pdf-zipper-cli-linux-x64 --help
```

### From Source
```bash
git clone https://github.com/your-username/pdf-zipper.git
cd pdf-zipper
pip install -e .
```

### Using Installation Script
```bash
git clone https://github.com/your-username/pdf-zipper.git
cd pdf-zipper
./install.sh
```
```bash
# Will be available after publishing to PyPI
pip install pdf-zipper
```

## 📖 Usage

### CLI Commands

After installation, you can use `pdf-zipper` or `pdfzip` commands:

```bash
# Launch GUI
pdf-zipper gui

# Compress PDF to specific size (auto mode)
pdf-zipper compress input.pdf --target-size 5.0

# Compress PDF with specific DPI (manual mode)
pdf-zipper compress input.pdf --dpi 150

# Convert PDF to PowerPoint
pdf-zipper convert input.pdf

# Show PDF information
pdf-zipper info input.pdf

# Show help
pdf-zipper --help
```

The CLI provides rich, colorful output with progress indicators and detailed information (see CLI screenshot above).

### GUI Mode
```bash
pdf-zipper gui
```

The GUI provides an intuitive interface with file browser, drag & drop support, and real-time progress logging (see screenshot above).

### Programmatic Usage
```python
from pdf_zipper import autocompress_pdf, compress_pdf, convert_to_ppt

# Auto compress to 5MB
autocompress_pdf("input.pdf", "output.pdf", 5.0, print)

# Manual compress with 150 DPI
compress_pdf("input.pdf", "output.pdf", 150, print)

# Convert to PowerPoint
convert_to_ppt("input.pdf", "output.pptx", 150, print)
```

## 🛠️ Development

### Setup Development Environment
```bash
git clone https://github.com/your-username/pdf-zipper.git
cd pdf-zipper
pip install -e ".[dev]"
```

### Run Tests
```bash
pytest
```

### Code Formatting
```bash
black src/
isort src/
```

## 📋 Requirements

- Python 3.8+
- PyMuPDF (fitz)
- Pillow
- python-pptx
- rich
- textual
- typer

## 🔧 How It Works

1. **Auto Compression**: Uses binary search to find the optimal DPI that achieves the target file size
2. **Manual Compression**: Converts PDF pages to images at specified DPI and recreates the PDF
3. **PDF to PPT**: Extracts each page as an image and creates PowerPoint slides

## 💡 Tips

- Higher DPI = better quality but larger file size
- Auto compression may take longer but provides precise size control
- For best results, start with the auto compression feature
- Use the GUI for interactive file selection and real-time progress
- Use CLI for batch processing and automation

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
