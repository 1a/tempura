#!/bin/bash
# Installation script for Tempura Weather CLI

set -e

echo "========================================"
echo "🌤️  Installing Tempura Weather CLI"
echo "========================================"
echo ""

# Check Python version
echo "📋 Checking Python version..."
PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
echo "   Python $PYTHON_VERSION detected"

if ! python3 -c 'import sys; exit(0 if sys.version_info >= (3, 10) else 1)'; then
    echo "❌ Error: Python 3.10 or higher is required"
    exit 1
fi

echo "✅ Python version OK"
echo ""

# Install with pip
echo "📦 Installing Tempura..."
cd "$(dirname "$0")"

# Install in editable mode so the 'tempura' command is available
pip3 install -e . --quiet

if [ $? -eq 0 ]; then
    echo "✅ Installation successful!"
    echo ""
    echo "========================================"
    echo "🎉 Tempura is now installed!"
    echo "========================================"
    echo ""
    echo "📝 To get started:"
    echo ""
    echo "   1. Get a free API key from:"
    echo "      https://openweathermap.org/api"
    echo ""
    echo "   2. Run the app:"
    echo "      tempura"
    echo ""
    echo "   3. Or use CLI mode:"
    echo "      tempura-cli current \"San Francisco\""
    echo ""
    echo "💡 The first time you run 'tempura', you'll be"
    echo "   guided through a quick setup wizard."
    echo ""
else
    echo "❌ Installation failed"
    exit 1
fi
