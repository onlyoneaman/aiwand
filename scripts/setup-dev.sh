#!/bin/bash
# Development environment setup script for AIWand

set -e  # Exit on any error

echo "🪄 AIWand Development Setup"
echo "=========================="

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not found. Please install Python 3.8+ first."
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv .venv
    echo "✅ Virtual environment created"
else
    echo "📦 Virtual environment already exists"
fi

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source .venv/bin/activate

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip

# Install package in development mode
echo "📥 Installing AIWand in development mode..."
pip install -e ".[dev]"

# Run tests to verify installation
echo "🧪 Running installation tests..."
python test_install.py

echo ""
echo "🎉 Setup complete! To activate the environment, run:"
echo "   source .venv/bin/activate"
echo ""
echo "📝 Available commands:"
echo "   python test_install.py          # Test installation"
echo "   python examples/basic_usage.py  # Run examples"
echo "   aiwand --help                   # CLI help"
echo "   pip install -e .                # Reinstall after changes"
echo ""
echo "🔧 Don't forget to set your API key:"
echo "   export OPENAI_API_KEY='your-key'     # For OpenAI" 
echo "   export GEMINI_API_KEY='your-key'     # For Gemini" 