@echo off
echo 🚀 LAUNCHING SURGICALLY FIXED AI MENTOR SYSTEM...
echo ====================================================

cd /d "E:\MEM_AGENT"

echo 🔧 Activating virtual environment...
call .\venv\Scripts\activate.bat

echo 🔑 Setting API key...
set GEMINI_API_KEY=AIzaSyDj-aTJt7riqX6MJSsW2Tu7uO8cjisEGqE

echo 🧠 Starting Surgically Fixed AI Mentor System...
echo System will be available at http://localhost:8501
echo ====================================================

.\venv\Scripts\streamlit.exe run surgically_fixed_ai_mentor.py --server.port 8501 --server.address 0.0.0.0

echo.
echo 🎉 System launch complete!
echo Access your AI Mentor at: http://localhost:8501
pause
