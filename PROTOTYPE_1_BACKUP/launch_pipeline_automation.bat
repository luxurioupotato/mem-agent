@echo off
echo ========================================
echo ENHANCED MEMORY AGENT PIPELINE AUTOMATION
echo ========================================
echo.

echo Starting Forever-Evolving AI System...
echo.

REM Navigate to project directory
cd /d "%~dp0"

REM Activate virtual environment
echo Activating virtual environment...
call .\venv\Scripts\activate.bat

REM Set API key
echo Setting up environment...
set GEMINI_API_KEY=AIzaSyDj-aTJt7riqX6MJSsW2Tu7uO8cjisEGqE

REM Install any missing dependencies
echo Installing Flask if needed...
.\venv\Scripts\pip.exe install flask --quiet

echo.
echo ========================================
echo SYSTEM FEATURES:
echo ========================================
echo • Persistent chat memory with SQLite
echo • Recursive prompt generation
echo • Advanced loop detection and pivot
echo • Gemini API integration
echo • Cursor AI autonomous initialization
echo • Comprehensive analytics
echo • RESTful API server
echo.
echo ========================================
echo API ENDPOINTS:
echo ========================================
echo • Main Chat: http://localhost:5000/chat
echo • Health Check: http://localhost:5000/health
echo • Documentation: http://localhost:5000/
echo • Analytics: http://localhost:5000/analytics
echo • Cursor AI Init: http://localhost:5000/cursor-ai/init
echo.
echo ========================================
echo STARTING PIPELINE AUTOMATION SUITE...
echo ========================================
echo.

REM Run the pipeline automation suite
.\venv\Scripts\python.exe pipeline_automation_suite.py

echo.
echo Pipeline automation stopped.
pause
