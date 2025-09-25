# launch_verified_ui.ps1 - Verified Setup and Boot Script
# Comprehensive verified setup for Advanced AI Memory Agent System

# Define project and script names
$projectDir = "E:\MEM_AGENT"
$scriptName = "enhanced_memory_agent_ui.py"

Write-Host "Advanced AI Memory Agent - Verified Setup and Boot" -ForegroundColor Green
Write-Host "====================================================" -ForegroundColor Gray

# Set working directory
Set-Location -Path $projectDir
Write-Host "Changed directory to $projectDir" -ForegroundColor Cyan

# Check if Streamlit script exists
if (-not (Test-Path $scriptName)) {
    Write-Host "ERROR: $scriptName not found in directory" -ForegroundColor Red
    Write-Host "Available Python files:" -ForegroundColor Yellow
    Get-ChildItem -Name "*.py" | ForEach-Object { Write-Host "  - $_" -ForegroundColor Cyan }
    pause
    exit 1
}

Write-Host "Script file verified: $scriptName" -ForegroundColor Green

# Setup virtual environment if missing
$venvPath = Join-Path $projectDir "venv"
$activateScript = Join-Path $venvPath "Scripts\Activate.ps1"

if (-not (Test-Path $venvPath)) {
    Write-Host "No virtual environment found, creating one..." -ForegroundColor Yellow
    python -m venv $venvPath
    if ($LASTEXITCODE -ne 0) {
        Write-Error "Failed to create virtual environment"
        pause
        exit 1
    }
}

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Green
try {
    & $activateScript
    Write-Host "Virtual environment activated successfully" -ForegroundColor Green
} catch {
    Write-Error "Failed to activate virtual environment. Check permissions."
    pause
    exit 1
}

# Upgrade pip and install dependencies
Write-Host "Upgrading pip, setuptools and wheel..." -ForegroundColor Yellow
python -m pip install --upgrade pip setuptools wheel

$reqFile = Join-Path $projectDir "requirements_rag.txt"
if (Test-Path $reqFile) {
    Write-Host "Installing requirements from requirements_rag.txt..." -ForegroundColor Yellow
    python -m pip install -r $reqFile
} else {
    Write-Host "Installing essential dependencies..." -ForegroundColor Yellow
    python -m pip install streamlit google-generativeai python-dotenv
}

# Load .env variables if present
$envFile = Join-Path $projectDir ".env"
if (Test-Path $envFile) {
    Write-Host "Loading environment variables..." -ForegroundColor Yellow
    Get-Content $envFile | ForEach-Object {
        if ($_ -match "^([^=]+)=(.+)$") {
            $name=$matches[1].Trim()
            $value=$matches[2].Trim()
            Set-Item -Path "env:$name" -Value $value
        }
    }
    Write-Host "Environment variables loaded from .env" -ForegroundColor Green
} else {
    Write-Host "Setting API key directly..." -ForegroundColor Yellow
    $env:GEMINI_API_KEY = "AIzaSyDj-aTJt7riqX6MJSsW2Tu7uO8cjisEGqE"
}

# System verification
Write-Host ""
Write-Host "System Verification:" -ForegroundColor Green
Write-Host "  Working Directory: $(Get-Location)" -ForegroundColor Cyan
Write-Host "  Python Version: $(python --version)" -ForegroundColor Cyan
Write-Host "  Script File: $(if(Test-Path $scriptName) {'Found'} else {'Missing'})" -ForegroundColor Cyan
Write-Host "  API Key: $(if($env:GEMINI_API_KEY) {'Set'} else {'Not Set'})" -ForegroundColor Cyan
Write-Host "  Virtual Environment: $(if(Test-Path $venvPath) {'Active'} else {'Missing'})" -ForegroundColor Cyan

# Check for modules.py (enhanced system)
if (Test-Path "modules.py") {
    Write-Host "  Module System: Found - Enhanced 21-module system will load" -ForegroundColor Green
} else {
    Write-Host "  Module System: Basic system will load" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "Launching Enhanced Memory Agent UI..." -ForegroundColor Green
Write-Host "Server will be available at:" -ForegroundColor Yellow
Write-Host "   Local: http://localhost:8501" -ForegroundColor Cyan
Write-Host "   Network: http://0.0.0.0:8501" -ForegroundColor Cyan
Write-Host ""
Write-Host "The system will auto-analyze your data and generate initial strategic workflow..." -ForegroundColor Yellow
Write-Host "Press Ctrl+C to stop the server when done." -ForegroundColor Yellow
Write-Host "====================================================" -ForegroundColor Gray

# Launch Streamlit
try {
    streamlit run $scriptName --server.port 8501 --server.address 0.0.0.0
} catch {
    Write-Host "Error launching Streamlit: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host "Trying alternative launch method..." -ForegroundColor Yellow
    python -m streamlit run $scriptName --server.port 8501 --server.address 0.0.0.0
}

Write-Host ""
Write-Host "Enhanced Memory Agent UI has stopped." -ForegroundColor Yellow
pause