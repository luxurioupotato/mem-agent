@echo off
echo 🚀 FINAL LAUNCH - ADVANCED MEMORY AGENT UI
echo =============================================
echo.

REM Navigate to correct directory
cd /d "E:\MEM_AGENT\MEMORY_AGENT_SYSTEM"
echo ✅ Changed to: %CD%

REM Activate virtual environment
call venv\Scripts\activate.bat
echo ✅ Virtual environment activated

REM Install/update essential packages
echo 📦 Installing essential packages...
pip install streamlit google-generativeai python-dotenv > nul 2>&1

REM Check if UI file exists
if exist "advanced_memory_agent_ui.py" (
    echo ✅ Advanced UI file found
) else (
    echo ❌ Advanced UI file not found
    pause
    exit /b 1
)

REM Set environment variable
set GEMINI_API_KEY=AIzaSyDj-aTJt7riqX6MJSsW2Tu7uO8cjisEGqE
echo ✅ API key configured

REM Launch Streamlit
echo.
echo 🚀 Launching Advanced Memory Agent UI...
echo 🌐 Opening at: http://localhost:8501
echo 💡 Features: Chat, File Upload, Knowledge Base, Module Controls
echo ⏹️  Press Ctrl+C to stop
echo.

streamlit run advanced_memory_agent_ui.py --server.port 8501 --server.headless false

echo.
echo 🛑 Memory Agent UI stopped
pause
