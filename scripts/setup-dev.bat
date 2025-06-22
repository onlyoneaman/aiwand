@echo off
REM Development environment setup script for AIWand (Windows)

echo 🪄 AIWand Development Setup
echo ==========================

REM Check if Python is available
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python 3 is required but not found. Please install Python 3.8+ first.
    pause
    exit /b 1
)

REM Create virtual environment if it doesn't exist
if not exist ".venv" (
    echo 📦 Creating virtual environment...
    python -m venv .venv
    echo ✅ Virtual environment created
) else (
    echo 📦 Virtual environment already exists
)

REM Activate virtual environment
echo 🔄 Activating virtual environment...
call .venv\Scripts\activate.bat

REM Upgrade pip
echo ⬆️  Upgrading pip...
python -m pip install --upgrade pip

REM Install package in development mode
echo 📥 Installing AIWand in development mode...
pip install -e ".[dev]"

REM Run tests to verify installation
echo 🧪 Running installation tests...
python test_install.py

echo.
echo 🎉 Setup complete! To activate the environment, run:
echo    .venv\Scripts\activate.bat
echo.
echo 📝 Available commands:
echo    python test_install.py          # Test installation
echo    python examples/basic_usage.py  # Run examples
echo    aiwand --help                   # CLI help
echo    pip install -e .                # Reinstall after changes
echo.
echo 🔧 Don't forget to set your API key:
echo    set OPENAI_API_KEY=your-key     # For OpenAI
echo    set GEMINI_API_KEY=your-key     # For Gemini

pause 