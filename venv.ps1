# Check if venv exists
if (Test-Path ".\venv\Scripts\Activate.ps1") {
    Write-Host "Activating State of Decay 2 AI Environment..." -ForegroundColor Cyan
    # This 'dots' the script, which keeps the environment active in your current window
    . .\venv\Scripts\Activate.ps1
} else {
    Write-Host "Error: venv not found. Did you run 'py -3.11 -m venv venv'?" -ForegroundColor Red
}