@echo off
echo 🚀 LAUNCHING DUAL AI SYSTEM OPERATION
echo ================================================================
echo 🧠 SURGICALLY FIXED AI MENTOR + ⚡ INTELLIGENT AGENTIC CLUSTER
echo ================================================================

cd /d "E:\MEM_AGENT"

echo 🔧 Activating virtual environment...
call .\venv\Scripts\activate.bat

echo 🔑 Setting API key for both systems...
set GEMINI_API_KEY=AIzaSyDj-aTJt7riqX6MJSsW2Tu7uO8cjisEGqE

echo.
echo 🧠 SYSTEM 1: SURGICALLY FIXED AI MENTOR
echo ================================================================
echo 🎯 Strategic Business Mentor with Military-Grade Processing
echo 🌐 Access: http://localhost:8501
echo 🔥 Features: Advanced commands, revenue optimization, strategic guidance
echo ================================================================

start "AI Mentor System" cmd /k ".\venv\Scripts\streamlit.exe run surgically_fixed_ai_mentor.py --server.port 8501 --server.address 0.0.0.0"

echo.
echo ⏱️ Waiting 5 seconds for first system to initialize...
timeout /t 5 /nobreak >nul

echo.
echo ⚡ SYSTEM 2: INTELLIGENT AGENTIC CLUSTER
echo ================================================================
echo 🤖 Autonomous Software Engineering Agent with Level 3-4 Autonomy
echo 🌐 Access: http://localhost:8502
echo 🧠 Features: Maximum adaptive combinations, surgical precision, cognitive intelligence
echo ================================================================

start "Agentic Cluster System" cmd /k ".\venv\Scripts\streamlit.exe run intelligent_agentic_cluster_system.py --server.port 8502 --server.address 0.0.0.0"

echo.
echo ⏱️ Waiting 5 seconds for second system to initialize...
timeout /t 5 /nobreak >nul

echo.
echo 🎉 DUAL SYSTEM LAUNCH COMPLETE!
echo ================================================================
echo 🧠 AI MENTOR SYSTEM: http://localhost:8501
echo    • Strategic business guidance with revenue optimization
echo    • Military-grade processing with advanced commands
echo    • Professional mentor persona with measurable outcomes
echo.
echo ⚡ AGENTIC CLUSTER SYSTEM: http://localhost:8502  
echo    • Autonomous software engineering with surgical precision
echo    • Maximum adaptive combinations with cognitive intelligence
echo    • Level 3-4 autonomy with proactive cross-domain execution
echo ================================================================
echo.
echo 🎯 BOTH SYSTEMS READY FOR STRATEGIC BUSINESS EXECUTION!
echo 💰 Revenue Target: $10K-$20K monthly optimization
echo 🚀 Use both systems for maximum strategic advantage!
echo.
pause

