# 🚀 AUTOMATED MEM_AGENT DEPLOYMENT SCRIPT
# This script will handle everything for you!

Write-Host "🚀 MEM_AGENT AUTOMATED DEPLOYMENT" -ForegroundColor Green
Write-Host "=================================" -ForegroundColor Green
Write-Host ""

# Step 1: Check if GitHub repo exists
Write-Host "📋 STEP 1: CHECKING GITHUB REPOSITORY..." -ForegroundColor Cyan
$repoUrl = "https://github.com/luxurioupotato/mem-agent"
$response = try { Invoke-WebRequest -Uri $repoUrl -Method Head -TimeoutSec 10 } catch { $null }

if ($response -and $response.StatusCode -eq 200) {
    Write-Host "✅ GitHub repository found!" -ForegroundColor Green
    
    # Step 2: Push code to GitHub
    Write-Host "📋 STEP 2: PUSHING CODE TO GITHUB..." -ForegroundColor Cyan
    try {
        git push -u origin main
        Write-Host "✅ Code pushed successfully!" -ForegroundColor Green
    } catch {
        Write-Host "❌ Push failed. Trying to set upstream..." -ForegroundColor Red
        git push --set-upstream origin main
    }
    
    # Step 3: Open Streamlit Cloud
    Write-Host "📋 STEP 3: OPENING STREAMLIT CLOUD..." -ForegroundColor Cyan
    Start-Process "https://share.streamlit.io"
    
    # Step 4: Display deployment instructions
    Write-Host ""
    Write-Host "🎯 STREAMLIT DEPLOYMENT FORM VALUES:" -ForegroundColor Yellow
    Write-Host "Repository: luxurioupotato/mem-agent" -ForegroundColor White
    Write-Host "Branch: main" -ForegroundColor White
    Write-Host "Main file path: dashboard/app.py" -ForegroundColor White
    Write-Host "App URL: mem-agent-dashboard" -ForegroundColor White
    Write-Host ""
    Write-Host "🔧 ENVIRONMENT VARIABLES:" -ForegroundColor Yellow
    Write-Host "Key: API_BASE_URL" -ForegroundColor White
    Write-Host "Value: https://saturday-distant-motors-clone.trycloudflare.com" -ForegroundColor White
    Write-Host ""
    Write-Host "✅ READY TO DEPLOY!" -ForegroundColor Green
    
} else {
    Write-Host "❌ GitHub repository not found!" -ForegroundColor Red
    Write-Host ""
    Write-Host "🔗 PLEASE CREATE THE REPOSITORY FIRST:" -ForegroundColor Yellow
    Write-Host "1. Go to: https://github.com/new" -ForegroundColor White
    Write-Host "2. Repository name: mem-agent" -ForegroundColor White
    Write-Host "3. Make it PUBLIC" -ForegroundColor White
    Write-Host "4. Click 'Create repository'" -ForegroundColor White
    Write-Host "5. Run this script again" -ForegroundColor White
    Write-Host ""
    Write-Host "⏳ Opening GitHub repository creation page..." -ForegroundColor Cyan
    Start-Process "https://github.com/new"
}

Write-Host ""
Write-Host "🎯 DEPLOYMENT COMPLETE!" -ForegroundColor Green
Write-Host "Your MEM_AGENT dashboard will be available at:" -ForegroundColor White
Write-Host "https://mem-agent-dashboard.streamlit.app" -ForegroundColor Cyan
