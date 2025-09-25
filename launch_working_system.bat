@echo off
:: WORKING SYSTEM LAUNCHER - SURGICALLY INTEGRATED UI
:: Launches the verified working version with proper hosting

echo.
echo ================================================================
echo 🚀 LAUNCHING SURGICALLY INTEGRATED UI SYSTEM
echo ================================================================
echo 🏆 VERIFIED WORKING VERSION WITH PROPER HOSTING
echo ================================================================

:: Activate virtual environment
call .\venv\Scripts\activate

:: Set API key
set GEMINI_API_KEY=AIzaSyDj-aTJt7riqX6MJSsW2Tu7uO8cjisEGqE

echo.
echo 📋 SYSTEM FEATURES:
echo ================================================================
echo • Surgically integrated Enhanced Memory Agent UI
echo • Proper asyncio integration with Streamlit
echo • 5 Strategic Clusters with 21 specialized modules
echo • Advanced error handling and recovery
echo • Production-ready architecture
echo ================================================================

echo.
echo 🌐 LAUNCHING STREAMLIT UI...
echo ================================================================
echo • Access: http://localhost:8501
echo • System: Surgically Integrated Enhanced Memory Agent
echo • Status: Production-ready with best practices
echo ================================================================

echo.
echo 🎉 STARTING WORKING SYSTEM...
streamlit run surgically_integrated_ui.py --server.port 8501 --server.address localhost

pause
