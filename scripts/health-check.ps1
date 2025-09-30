<#
  MEM_AGENT Health Check (Windows/PowerShell)
  - Verifies Docker Desktop and compose services
  - Checks API, n8n, Mautic health endpoints
  Usage:
    pwsh -File scripts/health-check.ps1
#>

param(
  [string]$ApiUrl = "http://localhost:8000",
  [string]$N8nUrl = "http://localhost:5678",
  [string]$MauticUrl = "http://localhost:8888"
)

function Test-Endpoint {
  param([string]$Url)
  try {
    $r = Invoke-WebRequest -Uri $Url -UseBasicParsing -TimeoutSec 8
    return @{ ok = $true; status = $r.StatusCode; url = $Url }
  } catch {
    return @{ ok = $false; status = $_.Exception.Message; url = $Url }
  }
}

Write-Host "🔎 MEM_AGENT Health Check" -ForegroundColor Cyan

# 1) Docker engine
Write-Host "1) Checking Docker engine..." -NoNewline
try {
  $null = docker info 2>$null
  Write-Host " OK" -ForegroundColor Green
} catch {
  Write-Host " FAIL" -ForegroundColor Red
  Write-Host "   ➜ Start Docker Desktop and re-run." -ForegroundColor Yellow
  exit 1
}

# 2) Compose services
Write-Host "2) Checking compose services (docker compose ps)..."
try {
  docker compose ps
} catch {
  Write-Host "   ➜ Run from project root (E:\MEM_AGENT) and ensure docker-compose.yml exists." -ForegroundColor Yellow
}

# 3) API health
Write-Host "3) Checking API health..." -NoNewline
$api = Test-Endpoint "$ApiUrl/health"
if ($api.ok) { Write-Host " OK ($($api.status))" -ForegroundColor Green } else { Write-Host " FAIL ($($api.status))" -ForegroundColor Red }

# 4) n8n UI
Write-Host "4) Checking n8n UI..." -NoNewline
$n8n = Test-Endpoint $N8nUrl
if ($n8n.ok) { Write-Host " OK ($($n8n.status))" -ForegroundColor Green } else { Write-Host " FAIL ($($n8n.status))" -ForegroundColor Red }

# 5) Mautic UI
Write-Host "5) Checking Mautic UI..." -NoNewline
$mautic = Test-Endpoint $MauticUrl
if ($mautic.ok) { Write-Host " OK ($($mautic.status))" -ForegroundColor Green } else { Write-Host " FAIL ($($mautic.status))" -ForegroundColor Red }

Write-Host ""; Write-Host "Summary:" -ForegroundColor Cyan
Write-Host ("- API    : {0} -> {1}" -f ($api.ok?"OK":"FAIL"), $api.url)
Write-Host ("- n8n    : {0} -> {1}" -f ($n8n.ok?"OK":"FAIL"), $n8n.url)
Write-Host ("- Mautic : {0} -> {1}" -f ($mautic.ok?"OK":"FAIL"), $mautic.url)

if (-not $api.ok -or -not $n8n.ok -or -not $mautic.ok) { exit 2 } else { exit 0 }

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
