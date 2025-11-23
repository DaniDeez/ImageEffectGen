#!/bin/bash
# Simple installation script for ImageEffectGen

echo "=========================================="
echo "ImageEffectGen - Installation"
echo "=========================================="
echo ""

# Check Python version
echo "Checking Python version..."
python3 --version
if [ $? -ne 0 ]; then
    echo "Error: Python 3 is not installed!"
    exit 1
fi
echo ""

# Check pip
echo "Checking pip..."
pip --version
if [ $? -ne 0 ]; then
    echo "Error: pip is not installed!"
    exit 1
fi
echo ""

# Install dependencies
echo "Installing dependencies..."
echo "This may take a few minutes..."
echo ""
pip install -r requirements.txt

if [ $? -eq 0 ]; then
    echo ""
    echo "=========================================="
    echo "✓ Installation Complete!"
    echo "=========================================="
    echo ""
    echo "Next steps:"
    echo "  1. Run demo:          python demo.py"
    echo "  2. Use with image:    python run_filter.py your_image.jpg"
    echo "  3. See quick guide:   cat QUICKSTART.md"
    echo ""
else
    echo ""
    echo "✗ Installation failed!"
    echo "Try running manually: pip install -r requirements.txt"
    exit 1
fi
