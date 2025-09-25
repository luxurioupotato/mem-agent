# PowerShell script to launch Memory Agent UI
# Automates all steps for proper activation and launch

Write-Host "🚀 LAUNCHING SSI-ENHANCED MEMORY AGENT UI" -ForegroundColor Green
Write-Host "=" * 50

# Step 1: Set execution policy if needed
try {
    Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser -Force
    Write-Host "✅ Execution policy set" -ForegroundColor Green
} catch {
    Write-Host "⚠️ Execution policy already set or failed: $($_.Exception.Message)" -ForegroundColor Yellow
}

# Step 2: Navigate to correct directory
$ProjectDir = "E:\MEM_AGENT\MEMORY_AGENT_SYSTEM"
Set-Location $ProjectDir
Write-Host "✅ Changed to directory: $ProjectDir" -ForegroundColor Green

# Step 3: Check if virtual environment exists
if (Test-Path ".\venv\Scripts\Activate.ps1") {
    Write-Host "✅ Virtual environment found" -ForegroundColor Green
} else {
    Write-Host "❌ Virtual environment not found. Creating..." -ForegroundColor Red
    python -m venv venv
    Write-Host "✅ Virtual environment created" -ForegroundColor Green
}

# Step 4: Activate virtual environment
try {
    & ".\venv\Scripts\Activate.ps1"
    Write-Host "✅ Virtual environment activated" -ForegroundColor Green
} catch {
    Write-Host "❌ Failed to activate virtual environment: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}

# Step 5: Install dependencies
Write-Host "📦 Installing dependencies..." -ForegroundColor Cyan
pip install streamlit google-generativeai python-dotenv

# Step 6: Check if UI file exists
if (Test-Path "all_in_one_memory_agent_ui.py") {
    Write-Host "✅ UI file found" -ForegroundColor Green
} else {
    Write-Host "❌ UI file not found" -ForegroundColor Red
    exit 1
}

# Step 7: Launch Streamlit
Write-Host "🚀 Launching Streamlit UI..." -ForegroundColor Green
Write-Host "🌐 Opening at: http://localhost:8501" -ForegroundColor Cyan
Write-Host "⏹️ Press Ctrl+C to stop" -ForegroundColor Yellow
Write-Host ""

streamlit run all_in_one_memory_agent_ui.py --server.port 8501
