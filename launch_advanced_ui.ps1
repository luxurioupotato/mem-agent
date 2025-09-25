# launch_advanced_ui.ps1 - Advanced Memory Agent UI Launcher
# Simple and clean launcher script

Write-Host "Advanced Memory Agent - System Launcher" -ForegroundColor Green
Write-Host "===============================================" -ForegroundColor Gray

# Set working directory to the script location
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
$ProjectDir = Join-Path $ScriptDir "MEMORY_AGENT_SYSTEM"

Write-Host "Script Directory: $ScriptDir" -ForegroundColor Yellow
Write-Host "Project Directory: $ProjectDir" -ForegroundColor Yellow

# Check if project directory exists
if (-not (Test-Path $ProjectDir)) {
    Write-Host "Error: MEMORY_AGENT_SYSTEM directory not found at $ProjectDir" -ForegroundColor Red
    Write-Host "Please ensure you're running this script from the correct location." -ForegroundColor Red
    pause
    exit 1
}

# Change to project directory
Set-Location $ProjectDir
Write-Host "Changed to project directory: $(Get-Location)" -ForegroundColor Green

# Check if virtual environment exists
$VenvPath = Join-Path $ProjectDir "venv"
if (-not (Test-Path $VenvPath)) {
    Write-Host "Creating virtual environment..." -ForegroundColor Yellow
    python -m venv venv
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Failed to create virtual environment" -ForegroundColor Red
        pause
        exit 1
    }
    Write-Host "Virtual environment created" -ForegroundColor Green
}

# Activate virtual environment
$ActivateScript = Join-Path $VenvPath "Scripts\Activate.ps1"
if (Test-Path $ActivateScript) {
    Write-Host "Activating virtual environment..." -ForegroundColor Yellow
    & $ActivateScript
    Write-Host "Virtual environment activated" -ForegroundColor Green
} else {
    Write-Host "Virtual environment activation script not found" -ForegroundColor Red
    pause
    exit 1
}

# Set API key environment variable
$env:GEMINI_API_KEY = "AIzaSyDj-aTJt7riqX6MJSsW2Tu7uO8cjisEGqE"
Write-Host "Gemini API key configured" -ForegroundColor Green

# Check if advanced UI file exists
$UIFile = "advanced_memory_agent_ui.py"
if (-not (Test-Path $UIFile)) {
    Write-Host "Error: $UIFile not found in $(Get-Location)" -ForegroundColor Red
    Write-Host "Available Python files:" -ForegroundColor Yellow
    Get-ChildItem -Name "*.py" | ForEach-Object { Write-Host "  - $_" -ForegroundColor Cyan }
    pause
    exit 1
}

# Install/upgrade dependencies
Write-Host "Installing/upgrading dependencies..." -ForegroundColor Yellow
python -m pip install --upgrade pip setuptools wheel
python -m pip install streamlit google-generativeai python-dotenv
Write-Host "Dependencies installed" -ForegroundColor Green

# Display system information
Write-Host ""
Write-Host "System Information:" -ForegroundColor Green
Write-Host "  Working Directory: $(Get-Location)" -ForegroundColor Cyan
Write-Host "  Python Version: $(python --version)" -ForegroundColor Cyan
Write-Host "  API Key: $(if($env:GEMINI_API_KEY) {'Set'} else {'Not Set'})" -ForegroundColor Cyan
Write-Host "  UI File: $(if(Test-Path $UIFile) {'Found'} else {'Missing'})" -ForegroundColor Cyan

Write-Host ""
Write-Host "Launching Advanced Memory Agent UI..." -ForegroundColor Green
Write-Host "Server will be available at:" -ForegroundColor Yellow
Write-Host "   Local: http://localhost:8501" -ForegroundColor Cyan
Write-Host "   Network: http://0.0.0.0:8501" -ForegroundColor Cyan
Write-Host ""
Write-Host "Press Ctrl+C to stop the server when you're done." -ForegroundColor Yellow
Write-Host "===============================================" -ForegroundColor Gray

# Launch Streamlit
try {
    streamlit run $UIFile --server.port 8501 --server.address 0.0.0.0
} catch {
    Write-Host "Error launching Streamlit: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host "Trying alternative launch method..." -ForegroundColor Yellow
    python -m streamlit run $UIFile --server.port 8501 --server.address 0.0.0.0
}

Write-Host ""
Write-Host "Advanced Memory Agent UI has stopped." -ForegroundColor Yellow
pause