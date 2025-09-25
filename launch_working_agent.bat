@echo off
cd /d "E:\MEM_AGENT"
call .\venv\Scripts\activate.bat
set GEMINI_API_KEY=AIzaSyDj-aTJt7riqX6MJSsW2Tu7uO8cjisEGqE
echo Starting Working Memory Agent...
echo System will be available at http://localhost:8501
.\venv\Scripts\streamlit.exe run working_memory_agent.py --server.port 8501 --server.address 0.0.0.0
pause
