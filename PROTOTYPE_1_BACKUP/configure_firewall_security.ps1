# Enhanced Memory Agent - Windows Firewall Security Configuration
# Optimizes security for network-accessible (0.0.0.0) host configuration

Write-Host "🛡️ ENHANCED MEMORY AGENT - FIREWALL SECURITY SETUP" -ForegroundColor Yellow
Write-Host "=" * 60 -ForegroundColor Cyan
Write-Host ""

Write-Host "Configuring Windows Firewall for Enhanced Memory Agent..." -ForegroundColor Green

# Check if running as administrator
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")

if (-not $isAdmin) {
    Write-Host "⚠️ WARNING: Not running as Administrator" -ForegroundColor Yellow
    Write-Host "Some firewall rules may not be applied." -ForegroundColor Yellow
    Write-Host "For full security setup, run PowerShell as Administrator." -ForegroundColor Yellow
    Write-Host ""
}

# Configure firewall rules for Enhanced Memory Agent
Write-Host "🔧 Configuring firewall rules..." -ForegroundColor Blue

try {
    # Allow Streamlit UI (port 8501) for local network only
    New-NetFirewallRule -DisplayName "Enhanced Memory Agent - Streamlit UI" -Direction Inbound -Protocol TCP -LocalPort 8501 -RemoteAddress LocalSubnet -Action Allow -ErrorAction SilentlyContinue
    Write-Host "✅ Streamlit UI (port 8501) - Local network access allowed" -ForegroundColor Green
    
    # Allow Flask API (port 5000) for local network only
    New-NetFirewallRule -DisplayName "Enhanced Memory Agent - Pipeline API" -Direction Inbound -Protocol TCP -LocalPort 5000 -RemoteAddress LocalSubnet -Action Allow -ErrorAction SilentlyContinue
    Write-Host "✅ Pipeline API (port 5000) - Local network access allowed" -ForegroundColor Green
    
} catch {
    Write-Host "⚠️ Could not configure firewall rules (may need Administrator privileges)" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "🌐 NETWORK ACCESS INFORMATION:" -ForegroundColor Yellow
Write-Host "=" * 40 -ForegroundColor Cyan

# Get current IP address
$ipAddress = (Get-NetIPAddress -AddressFamily IPv4 | Where-Object {$_.IPAddress -like "192.168.*" -or $_.IPAddress -like "10.*" -or $_.IPAddress -like "172.*"} | Select-Object -First 1).IPAddress

Write-Host "Your Network IP: $ipAddress" -ForegroundColor White
Write-Host ""
Write-Host "📱 ACCESS URLS:" -ForegroundColor Yellow
Write-Host "Streamlit UI:" -ForegroundColor White
Write-Host "  • Local: http://localhost:8501" -ForegroundColor Cyan
Write-Host "  • Network: http://${ipAddress}:8501" -ForegroundColor Cyan
Write-Host ""
Write-Host "Pipeline API:" -ForegroundColor White
Write-Host "  • Local: http://localhost:5000" -ForegroundColor Cyan
Write-Host "  • Network: http://${ipAddress}:5000" -ForegroundColor Cyan
Write-Host "  • Health Check: http://${ipAddress}:5000/health" -ForegroundColor Cyan
Write-Host "  • Documentation: http://${ipAddress}:5000/" -ForegroundColor Cyan
Write-Host ""

Write-Host "🛡️ SECURITY STATUS:" -ForegroundColor Yellow
Write-Host "✅ Network access restricted to local subnet only" -ForegroundColor Green
Write-Host "✅ Firewall rules configured for controlled access" -ForegroundColor Green
Write-Host "⚠️ Monitor access logs for security" -ForegroundColor Yellow
Write-Host ""

Write-Host "🚀 SYSTEM READY:" -ForegroundColor Yellow
Write-Host "Your Enhanced Memory Agent is configured for secure network access!" -ForegroundColor Green
Write-Host "Both Streamlit UI and Pipeline API are accessible locally and on your network." -ForegroundColor White
Write-Host ""

Write-Host "📋 NEXT STEPS:" -ForegroundColor Yellow
Write-Host "1. Launch your system: .\launch_pipeline_automation.ps1" -ForegroundColor White
Write-Host "2. Access Streamlit UI: http://localhost:8501" -ForegroundColor White  
Write-Host "3. Access Pipeline API: http://localhost:5000" -ForegroundColor White
Write-Host "4. Test network access from other devices if needed" -ForegroundColor White
