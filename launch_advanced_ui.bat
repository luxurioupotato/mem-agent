@echo off
REM Launch PowerShell script from batch file

REM Get the directory where this batch file resides
SET BATCHDIR=%~dp0

REM Full path to PowerShell script
SET PS_SCRIPT="%BATCHDIR%launch_advanced_ui.ps1"

REM Run the PowerShell script with execution policy bypass
powershell.exe -NoProfile -ExecutionPolicy Bypass -Command "& %PS_SCRIPT%"

REM Keep window open to see any messages
pause
