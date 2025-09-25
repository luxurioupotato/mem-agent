@echo off
:: ENHANCED SSI CONTROLLED SYSTEM LAUNCHER
:: Fixed response system with controlled startup, standby, and resume flow

echo.
echo ================================================================
echo 🚀 ENHANCED SSI CONTROLLED SYSTEM - RESPONSE SYSTEM FIXED
echo ================================================================
echo 🛡️ CONTROLLED STARTUP • STANDBY • RESUME FLOW
echo ================================================================

:: Activate virtual environment
if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate
    echo ✅ Virtual environment activated
) else (
    echo ⚠️ Creating new virtual environment...
    python -m venv venv
    call venv\Scripts\activate
    echo ✅ New virtual environment created and activated
)

:: Set API key
set GEMINI_API_KEY=AIzaSyDj-aTJt7riqX6MJSsW2Tu7uO8cjisEGqE

echo.
echo 🔧 RESPONSE SYSTEM FIXES APPLIED:
echo ================================================================
echo ✅ Controlled Startup Sequence - Proper initialization flow
echo ✅ Standby Mode Implementation - System waits for resume command
echo ✅ Enhanced Error Handling - Comprehensive error recovery
echo ✅ Master Analysis Integration - Complete framework operational
echo ✅ Dynamic Response Modes - Professional, Casual, Technical, Master
echo ✅ SSI V1 High Alert Protocols - Maximum protection active
echo ================================================================

echo.
echo 🎯 CONTROLLED FLOW FEATURES:
echo ================================================================
echo 🔄 Startup Sequence - Complete resource loading and diagnostics
echo 💾 Automatic Backup - Comprehensive state preservation
echo 🔍 System Audit - In-depth health and compliance verification
echo 🛡️ Standby Mode - Controlled activation requiring resume command
echo 🎨 Dynamic Modes - Intelligent response mode detection
echo ================================================================

echo.
echo 🔧 Installing dependencies...
pip install streamlit google-generativeai python-dotenv

echo.
echo 🌐 LAUNCHING ENHANCED SSI CONTROLLED SYSTEM...
echo ================================================================
echo • Access: http://localhost:8501
echo • System: Enhanced SSI Controlled with Fixed Response System
echo • Features: Controlled startup, standby mode, dynamic responses
echo • Protection: SSI V1 High Alert Protocols Active
echo ================================================================

echo.
echo 🎉 STARTING ENHANCED SSI CONTROLLED SYSTEM...
streamlit run enhanced_ssi_controlled_system.py --server.port 8501 --server.address localhost

pause

