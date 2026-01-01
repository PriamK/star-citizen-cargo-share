#!/bin/bash
# ========================================
# Star Citizen Cargo Share - Build Script
# For Linux/macOS
# ========================================

echo ""
echo "╔═══════════════════════════════════════════════════════════╗"
echo "║   ⬢ STAR CITIZEN CARGO SHARE - BUILD EXECUTABLE ⬢       ║"
echo "╚═══════════════════════════════════════════════════════════╝"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "[ERROR] Python 3 is not installed"
    echo "Please install Python 3.7+ from https://www.python.org/"
    exit 1
fi

echo "[1/4] Installing PyInstaller..."
pip3 install pyinstaller>=6.0.0

echo ""
echo "[2/4] Cleaning previous builds..."
rm -rf build dist

echo ""
echo "[3/4] Building executable with PyInstaller..."
pyinstaller cargo-share.spec

echo ""
echo "[4/4] Build complete!"
echo ""

if [ -f "dist/StarCitizenCargoShare" ]; then
    echo "╔═══════════════════════════════════════════════════════════╗"
    echo "║                    ✓ BUILD SUCCESSFUL                     ║"
    echo "╚═══════════════════════════════════════════════════════════╝"
    echo ""
    echo "Executable location: dist/StarCitizenCargoShare"
    echo ""
else
    echo "╔═══════════════════════════════════════════════════════════╗"
    echo "║                    ✗ BUILD FAILED                         ║"
    echo "╚═══════════════════════════════════════════════════════════╝"
    echo ""
    echo "Please check the error messages above."
    echo ""
fi
