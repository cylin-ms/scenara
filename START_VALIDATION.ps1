# Meeting Classification Validation App - Quick Start
# ====================================================

Write-Host ""
Write-Host "=============================================================================" -ForegroundColor Cyan
Write-Host "  🎯 MEETING CLASSIFICATION VALIDATION APP" -ForegroundColor Green
Write-Host "=============================================================================" -ForegroundColor Cyan
Write-Host ""

# Check if Flask is installed
Write-Host "Checking dependencies..." -ForegroundColor Yellow
$flaskInstalled = python -c "import flask; print('installed')" 2>$null

if ($flaskInstalled -ne "installed") {
    Write-Host "⚠  Flask not found. Installing..." -ForegroundColor Yellow
    pip install flask
    if ($LASTEXITCODE -ne 0) {
        Write-Host "✗ Failed to install Flask" -ForegroundColor Red
        Write-Host ""
        Write-Host "Please install manually:" -ForegroundColor Yellow
        Write-Host "  pip install flask" -ForegroundColor White
        Write-Host ""
        exit 1
    }
    Write-Host "✓ Flask installed successfully" -ForegroundColor Green
} else {
    Write-Host "✓ Flask is already installed" -ForegroundColor Green
}

Write-Host ""
Write-Host "🚀 Starting validation server..." -ForegroundColor Green
Write-Host ""
Write-Host "📂 Working directory: $PWD" -ForegroundColor White
Write-Host "🌐 Open your browser to: http://localhost:5000" -ForegroundColor Cyan
Write-Host ""
Write-Host "⌨️  Press Ctrl+C to stop the server when done" -ForegroundColor Yellow
Write-Host ""
Write-Host "=============================================================================" -ForegroundColor Cyan
Write-Host ""

# Wait a moment
Start-Sleep -Seconds 1

# Start the app (with automatic browser opening)
python start_validation_app.py

Write-Host ""
Write-Host "✓ Server stopped. Validation results saved!" -ForegroundColor Green
Write-Host "📊 Results: experiments/2025-10-28/human_validation_results.json" -ForegroundColor White
Write-Host ""
