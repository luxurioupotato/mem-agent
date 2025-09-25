@echo off
echo Checking Advanced Memory Agent UI Status...
echo.

REM Check if port 8501 is listening
netstat -an | findstr :8501 > nul
if %errorlevel% == 0 (
    echo ✅ Port 8501 is active - UI should be running
    echo 🌐 Access your Advanced Memory Agent at: http://localhost:8501
) else (
    echo ❌ Port 8501 is not active - UI may not be running
    echo 💡 Try running launch_advanced_ui.bat to start the system
)

echo.
echo Press any key to continue...
pause > nul
