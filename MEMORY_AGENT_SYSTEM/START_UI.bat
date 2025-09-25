@echo off
echo 🚀 STARTING SSI-ENHANCED MEMORY AGENT UI
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://python.org
    pause
    exit /b 1
)

REM Check if API key is set
if "%GEMINI_API_KEY%"=="" (
    echo ❌ GEMINI_API_KEY not set
    echo Please set your API key:
    echo set GEMINI_API_KEY=your_api_key_here
    echo.
    echo Or set it now:
    set /p GEMINI_API_KEY="Enter your Gemini API key: "
)

REM Install required packages
echo 📦 Installing required packages...
pip install -r requirements_ui.txt >nul 2>&1

REM Start the UI
echo.
echo 🚀 Starting Memory Agent UI...
echo 🌐 The UI will open in your web browser
echo.
streamlit run streamlit_chat_ui.py

pause




