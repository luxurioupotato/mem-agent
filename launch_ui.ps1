# launch_ui.ps1 - Setup venv, install deps, launch Streamlit Gemini UI

Set-Location -Path "E:\MEM_AGENT\MEMORY_AGENT_SYSTEM"

Set-ExecutionPolicy RemoteSigned -Scope CurrentUser -Force

if (-Not (Test-Path ".\venv")) {
    Write-Host "Creating virtual environment..."
    python -m venv venv
}

$activate = ".\venv\Scripts\Activate.ps1"
if (Test-Path $activate) {
    Write-Host "Activating virtual environment..."
    & $activate
} else {
    Write-Error "Virtual environment activation script not found."
    exit 1
}

Write-Host "Upgrading pip and essential tools..."
python -m pip install --upgrade pip setuptools wheel

if (Test-Path ".\requirements_rag.txt") {
    Write-Host "Installing dependencies from requirements_rag.txt..."
    python -m pip install -r requirements_rag.txt
} else {
    Write-Host "Installing essential packages..."
    python -m pip install streamlit google-generativeai python-dotenv
}

Write-Host "Launching Gemini Advanced Memory Agent UI on port 8501..."
Write-Host "Access at: http://localhost:8501"
streamlit run gemini_advanced_memory_agent_ui.py --server.port 8501 --server.address 0.0.0.0