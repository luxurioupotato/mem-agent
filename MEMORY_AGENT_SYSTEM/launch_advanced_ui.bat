@echo off
cd /d "E:\MEM_AGENT\MEMORY_AGENT_SYSTEM"
call venv\Scripts\activate.bat
set GEMINI_API_KEY=AIzaSyDj-aTJt7riqX6MJSsW2Tu7uO8cjisEGqE
echo Starting Advanced Memory Agent UI...
echo Access at: http://localhost:8501
streamlit run advanced_memory_agent_ui.py --server.port 8501 --server.address 0.0.0.0
pause
