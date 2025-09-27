# Creates temporary public URLs via Cloudflare Tunnel (trycloudflare)
# Services: API (8000), n8n (5678), Mautic (8888)
# Usage: powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\hosted-access.ps1

$ErrorActionPreference = 'Stop'

function Ensure-Cloudflared {
  $cf = Join-Path $PSScriptRoot 'cloudflared.exe'
  if (Test-Path $cf) { return $cf }
  Write-Host "Downloading cloudflared..." -ForegroundColor Yellow
  $url = 'https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-windows-amd64.exe'
  Invoke-WebRequest -Uri $url -OutFile $cf -UseBasicParsing
  return $cf
}

function Start-Tunnel($cf, $name, $url, $logFile, $workDir) {
  Write-Host "Launching $name tunnel -> $url" -ForegroundColor Cyan
  $args = @('tunnel','--url', $url, '--logfile', $logFile, '--loglevel', 'info')
  Start-Process -FilePath $cf -ArgumentList $args -WorkingDirectory $workDir -WindowStyle Minimized
}

function Wait-And-Show-URL($logFile, $name) {
  Write-Host "Waiting for $name URL..." -ForegroundColor DarkGray
  $deadline = (Get-Date).AddSeconds(45)
  while ((Get-Date) -lt $deadline) {
    if (Test-Path $logFile) {
      $content = Get-Content $logFile -Raw
      $m = Select-String -InputObject $content -Pattern 'https?://[\w.-]+\.trycloudflare\.com' -AllMatches
      if ($m -and $m.Matches.Count -gt 0) {
        $url = $m.Matches[-1].Value
        Write-Host "$name public URL: $url" -ForegroundColor Green
        return $url
      }
    }
    Start-Sleep -Milliseconds 750
  }
  Write-Host "Could not detect $name URL yet. Check logs: $logFile" -ForegroundColor Yellow
}

try {
  $cf = Ensure-Cloudflared
  $logsDir = Join-Path $PSScriptRoot 'tunnel-logs'
  if (-not (Test-Path $logsDir)) { New-Item -ItemType Directory -Path $logsDir | Out-Null }

  # API
  $apiLog = Join-Path $logsDir 'api.log'
  Start-Tunnel $cf 'API' 'http://localhost:8000' $apiLog $logsDir
  $apiUrl = Wait-And-Show-URL $apiLog 'API'

  # n8n
  $n8nLog = Join-Path $logsDir 'n8n.log'
  Start-Tunnel $cf 'n8n' 'http://localhost:5678' $n8nLog $logsDir
  $n8nUrl = Wait-And-Show-URL $n8nLog 'n8n'

  # Mautic
  $mauticLog = Join-Path $logsDir 'mautic.log'
  Start-Tunnel $cf 'Mautic' 'http://localhost:8888' $mauticLog $logsDir
  $mauticUrl = Wait-And-Show-URL $mauticLog 'Mautic'

  Write-Host "\nHosted access ready:" -ForegroundColor Cyan
  Write-Host ("  API   : {0}" -f ($apiUrl   | ForEach-Object { $_ } ))
  Write-Host ("  n8n   : {0}" -f ($n8nUrl   | ForEach-Object { $_ } ))
  Write-Host ("  Mautic: {0}" -f ($mauticUrl| ForEach-Object { $_ } ))
  Write-Host "(Note: URLs are temporary; restarting this script will change them.)" -ForegroundColor DarkGray
} catch {
  Write-Host "Hosted access setup failed: $($_.Exception.Message)" -ForegroundColor Red
  exit 1
}
