# Requires: PowerShell 5+, Docker Desktop running

Write-Host "MEM_AGENT Health Check" -ForegroundColor Cyan

function Test-Http($url) {
  try {
    $resp = Invoke-WebRequest -Uri $url -UseBasicParsing -TimeoutSec 5
    return @{ ok = $true; status = $resp.StatusCode }
  } catch {
    return @{ ok = $false; error = $_.Exception.Message }
  }
}

# Docker services
Write-Host "\nChecking Docker services..." -ForegroundColor Yellow
try {
  docker compose ps
} catch {
  Write-Host "Docker not available: $($_.Exception.Message)" -ForegroundColor Red
}

# API endpoints
Write-Host "\nTesting API endpoints..." -ForegroundColor Yellow
$health = Test-Http "http://localhost:8000/health"
$stats  = Test-Http "http://localhost:8000/stats"

if ($health.ok) { Write-Host "API /health: $($health.status)" -ForegroundColor Green } else { Write-Host "API /health error: $($health.error)" -ForegroundColor Red }
if ($stats.ok) { Write-Host "API /stats: $($stats.status)" -ForegroundColor Green } else { Write-Host "API /stats error: $($stats.error)" -ForegroundColor Red }

# n8n UI
Write-Host "\nTesting n8n UI..." -ForegroundColor Yellow
$n8n = Test-Http "http://localhost:5678"
if ($n8n.ok) { Write-Host "n8n: $($n8n.status)" -ForegroundColor Green } else { Write-Host "n8n error: $($n8n.error)" -ForegroundColor Red }

# Mautic UI
Write-Host "\nTesting Mautic UI..." -ForegroundColor Yellow
$mautic = Test-Http "http://localhost:8888"
if ($mautic.ok) { Write-Host "Mautic: $($mautic.status)" -ForegroundColor Green } else { Write-Host "Mautic error: $($mautic.error)" -ForegroundColor Red }

Write-Host "\nDone." -ForegroundColor Cyan
