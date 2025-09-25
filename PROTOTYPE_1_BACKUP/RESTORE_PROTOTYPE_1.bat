@echo off
echo ========================================
echo PROTOTYPE 1 RESTORATION SCRIPT
echo ========================================
echo.

echo Restoring Enhanced Memory Agent System...
echo.

REM Navigate to parent directory
cd /d "%~dp0.."

echo Copying system files...
copy "PROTOTYPE_1_BACKUP\modules.py" "modules.py" /Y
copy "PROTOTYPE_1_BACKUP\orchestrator.py" "orchestrator.py" /Y
copy "PROTOTYPE_1_BACKUP\enhanced_memory_agent_ui.py" "enhanced_memory_agent_ui.py" /Y
copy "PROTOTYPE_1_BACKUP\surgically_integrated_ui.py" "surgically_integrated_ui.py" /Y
copy "PROTOTYPE_1_BACKUP\working_memory_agent.py" "working_memory_agent.py" /Y
copy "PROTOTYPE_1_BACKUP\comprehensive_boot_orchestrator.py" "comprehensive_boot_orchestrator.py" /Y
copy "PROTOTYPE_1_BACKUP\requirements_rag.txt" "requirements_rag.txt" /Y
copy "PROTOTYPE_1_BACKUP\.env" ".env" /Y
copy "PROTOTYPE_1_BACKUP\launch_working_agent.bat" "launch_working_agent.bat" /Y

echo.
echo Copying documentation...
copy "PROTOTYPE_1_BACKUP\BACKUP_RESTORATION_POINT_PROTOTYPE_1.md" "BACKUP_RESTORATION_POINT_PROTOTYPE_1.md" /Y
copy "PROTOTYPE_1_BACKUP\COMPREHENSIVE_README_PROTOTYPE_1.md" "COMPREHENSIVE_README_PROTOTYPE_1.md" /Y
copy "PROTOTYPE_1_BACKUP\FINAL_SURGICAL_STATUS_REPORT.md" "FINAL_SURGICAL_STATUS_REPORT.md" /Y
copy "PROTOTYPE_1_BACKUP\SURGICAL_ADJUSTMENTS_VERIFICATION.md" "SURGICAL_ADJUSTMENTS_VERIFICATION.md" /Y

echo.
echo Setting up virtual environment...
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

echo Activating virtual environment...
call .\venv\Scripts\activate.bat

echo Installing dependencies...
.\venv\Scripts\pip.exe install --upgrade pip setuptools wheel
.\venv\Scripts\pip.exe install -r requirements_rag.txt

echo.
echo Testing system components...
.\venv\Scripts\python.exe -c "import modules, orchestrator, working_memory_agent; print('✅ Core components verified')"
.\venv\Scripts\python.exe -c "import psutil, streamlit, google.generativeai; print('✅ Dependencies verified')"

echo.
echo ========================================
echo PROTOTYPE 1 RESTORATION COMPLETE
echo ========================================
echo.
echo System ready for launch!
echo Run: .\launch_working_agent.bat
echo Or access: http://localhost:8501
echo.
pause
