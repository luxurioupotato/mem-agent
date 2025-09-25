@echo off
echo 🚀 STARTING MEMORY AGENT UI
echo ============================

cd /d "E:\MEM_AGENT\MEMORY_AGENT_SYSTEM"
echo ✅ Changed to project directory

call venv\Scripts\activate.bat
echo ✅ Virtual environment activated

echo 📦 Installing/updating dependencies...
pip install streamlit google-generativeai python-dotenv

echo 🚀 Starting Memory Agent UI...
echo 🌐 Opening at: http://localhost:8501
echo ⏹️ Press Ctrl+C to stop
echo.

streamlit run all_in_one_memory_agent_ui.py --server.port 8501

pause
