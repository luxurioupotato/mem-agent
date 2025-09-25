# Enhanced Memory Agent Pipeline Automation Launcher
# Forever-evolving AI system with persistent memory and recursive self-improvement

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "ENHANCED MEMORY AGENT PIPELINE AUTOMATION" -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "🚀 Starting Forever-Evolving AI System..." -ForegroundColor Green
Write-Host ""

# Navigate to project directory
Set-Location -Path $PSScriptRoot

# Set execution policy
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser -Force

# Activate virtual environment
Write-Host "🔧 Activating virtual environment..." -ForegroundColor Blue
if (Test-Path ".\venv\Scripts\Activate.ps1") {
    & .\venv\Scripts\Activate.ps1
    Write-Host "✅ Virtual environment activated" -ForegroundColor Green
} else {
    Write-Error "❌ Virtual environment not found. Please run setup first."
    exit 1
}

# Set environment variables
Write-Host "⚙️ Setting up environment..." -ForegroundColor Blue
$env:GEMINI_API_KEY = "AIzaSyDj-aTJt7riqX6MJSsW2Tu7uO8cjisEGqE"

# Install Flask if not present
Write-Host "📦 Checking dependencies..." -ForegroundColor Blue
try {
    .\venv\Scripts\python.exe -c "import flask" 2>$null
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Installing Flask..." -ForegroundColor Yellow
        .\venv\Scripts\pip.exe install flask --quiet
        Write-Host "✅ Flask installed" -ForegroundColor Green
    }
} catch {
    Write-Host "Installing Flask..." -ForegroundColor Yellow
    .\venv\Scripts\pip.exe install flask --quiet
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "🎯 SYSTEM FEATURES:" -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "• 💾 Persistent chat memory with SQLite database" -ForegroundColor White
Write-Host "• 🔄 Recursive prompt generation with context awareness" -ForegroundColor White
Write-Host "• 🎯 Advanced loop detection and intelligent pivot" -ForegroundColor White
Write-Host "• 🤖 Gemini API integration with performance tracking" -ForegroundColor White
Write-Host "• 🚀 Cursor AI autonomous initialization integration" -ForegroundColor White
Write-Host "• 📊 Comprehensive analytics and health monitoring" -ForegroundColor White
Write-Host "• 🌐 RESTful API server for integration and deployment" -ForegroundColor White
Write-Host ""

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "🌐 API ENDPOINTS:" -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "• 💬 Main Chat: " -ForegroundColor White -NoNewline
Write-Host "http://localhost:5000/chat" -ForegroundColor Cyan
Write-Host "• ❤️ Health Check: " -ForegroundColor White -NoNewline
Write-Host "http://localhost:5000/health" -ForegroundColor Cyan
Write-Host "• 📚 Documentation: " -ForegroundColor White -NoNewline
Write-Host "http://localhost:5000/" -ForegroundColor Cyan
Write-Host "• 📊 Analytics: " -ForegroundColor White -NoNewline
Write-Host "http://localhost:5000/analytics" -ForegroundColor Cyan
Write-Host "• 🤖 Cursor AI Init: " -ForegroundColor White -NoNewline
Write-Host "http://localhost:5000/cursor-ai/init" -ForegroundColor Cyan
Write-Host ""

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "🎉 STARTING PIPELINE AUTOMATION SUITE..." -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "Press Ctrl+C to stop the server when done." -ForegroundColor Yellow
Write-Host ""

# Run the pipeline automation suite
try {
    .\venv\Scripts\python.exe pipeline_automation_suite.py
} catch {
    Write-Error "❌ Failed to start pipeline automation suite: $_"
    exit 1
}

Write-Host ""
Write-Host "👋 Pipeline automation stopped." -ForegroundColor Yellow
Write-Host "Press any key to continue..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
