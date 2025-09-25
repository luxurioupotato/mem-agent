@echo off
echo ========================================
echo PROTOTYPE 1 BACKUP VERIFICATION
echo ========================================
echo.

echo Verifying backup contents...
echo.

REM Check critical files
if exist "modules.py" (
    echo ✅ modules.py - FOUND
) else (
    echo ❌ modules.py - MISSING
)

if exist "orchestrator.py" (
    echo ✅ orchestrator.py - FOUND
) else (
    echo ❌ orchestrator.py - MISSING
)

if exist "working_memory_agent.py" (
    echo ✅ working_memory_agent.py - FOUND
) else (
    echo ❌ working_memory_agent.py - MISSING
)

if exist "comprehensive_boot_orchestrator.py" (
    echo ✅ comprehensive_boot_orchestrator.py - FOUND
) else (
    echo ❌ comprehensive_boot_orchestrator.py - MISSING
)

if exist "requirements_rag.txt" (
    echo ✅ requirements_rag.txt - FOUND
) else (
    echo ❌ requirements_rag.txt - MISSING
)

if exist ".env" (
    echo ✅ .env - FOUND
) else (
    echo ❌ .env - MISSING
)

if exist "launch_working_agent.bat" (
    echo ✅ launch_working_agent.bat - FOUND
) else (
    echo ❌ launch_working_agent.bat - MISSING
)

echo.
echo Checking documentation...

if exist "COMPREHENSIVE_README_PROTOTYPE_1.md" (
    echo ✅ COMPREHENSIVE_README_PROTOTYPE_1.md - FOUND
) else (
    echo ❌ COMPREHENSIVE_README_PROTOTYPE_1.md - MISSING
)

if exist "BACKUP_RESTORATION_POINT_PROTOTYPE_1.md" (
    echo ✅ BACKUP_RESTORATION_POINT_PROTOTYPE_1.md - FOUND
) else (
    echo ❌ BACKUP_RESTORATION_POINT_PROTOTYPE_1.md - MISSING
)

echo.
echo ========================================
echo BACKUP VERIFICATION COMPLETE
echo ========================================
echo.
echo To restore system, run: RESTORE_PROTOTYPE_1.bat
echo.
pause
