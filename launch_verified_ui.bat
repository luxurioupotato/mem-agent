@echo off
REM Verified Batch launcher for Enhanced Memory Agent System

echo ====================================================
echo Advanced AI Memory Agent - Verified System Launch
echo ====================================================
echo.

REM Determine batch directory
SET BATCHDIR=%~dp0

REM Full PowerShell script path
SET PS_SCRIPT="%BATCHDIR%launch_verified_ui.ps1"

echo Launching Enhanced Memory Agent System...
echo.

REM Run PowerShell script bypassing policy and profile
powershell.exe -NoProfile -ExecutionPolicy Bypass -Command "& %PS_SCRIPT%"

echo.
echo System launch completed.
pause