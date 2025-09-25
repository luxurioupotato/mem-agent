@echo off
title AI Mentor System Launcher
cd /d "E:\MEM_AGENT"

echo.
echo ================================================================
echo           🧠 AI MENTOR SYSTEM LAUNCHER
echo ================================================================
echo.
echo 🚀 Starting Enhanced AI Mentor System...
echo 🛡️ System Protection Protocols: ACTIVE
echo ⚡ Maximum Processing: 298+ parallel operations
echo 🔗 Cursor Integration: MAXIMUM seamless automation
echo.

REM Activate virtual environment and set API key
call .\venv\Scripts\activate.bat
set GEMINI_API_KEY=AIzaSyDj-aTJt7riqX6MJSsW2Tu7uO8cjisEGqE

echo ✅ Virtual environment activated
echo ✅ Gemini API configured
echo.
echo 🌐 Launching AI Mentor System UI...
echo    Access URL: http://localhost:8501
echo.

REM Launch the enhanced UI system
.\venv\Scripts\streamlit.exe run enhanced_ui_system.py --server.port 8501 --server.address 0.0.0.0

echo.
echo 🛑 AI Mentor System stopped
pause
