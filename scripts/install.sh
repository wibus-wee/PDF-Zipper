#!/bin/bash

# PDF Zipper Installation Script
# This script installs PDF Zipper and its dependencies

set -e

echo "🗜️ PDF Zipper Installation Script"
echo "=================================="

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed."
    echo "Please install Python 3.8 or later and try again."
    exit 1
fi

# Check Python version
python_version=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
echo "✅ Found Python $python_version"

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 is required but not installed."
    echo "Please install pip and try again."
    exit 1
fi

echo "✅ Found pip3"

# Install PDF Zipper
echo ""
echo "📦 Installing PDF Zipper..."

if [ -f "pyproject.toml" ]; then
    # Development installation
    echo "🔧 Installing in development mode..."
    pip3 install -e .
else
    # Production installation
    echo "🚀 Installing from PyPI..."
    pip3 install pdf-zipper
fi

echo ""
echo "🎉 Installation complete!"
echo ""
echo "📖 Usage:"
echo "  pdf-zipper --help          # Show help"
echo "  pdf-zipper gui             # Launch GUI"
echo "  pdf-zipper compress file.pdf  # Compress PDF"
echo "  pdf-zipper convert file.pdf   # Convert to PPT"
echo "  pdf-zipper info file.pdf      # Show PDF info"
echo ""
echo "🔗 For more information, visit: https://github.com/your-username/pdf-zipper"
