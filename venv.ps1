$VENV_PATH = ".\venv"

# 1. Check if the venv directory exists
if (-not (Test-Path $VENV_PATH)) {
    Write-Host "Virtual environment not found. Creating it now with Python 3.11..." -ForegroundColor Yellow
    
    # Create the venv using the py launcher to target 3.11 specifically
    py -3.11 -m venv venv
    
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Error: Failed to create venv. Ensure Python 3.11 is installed." -ForegroundColor Red
        return
    }
    
    Write-Host "Successfully created venv at $VENV_PATH" -ForegroundColor Green
}

# 2. Activate the environment
$ACTIVATE_SCRIPT = "$VENV_PATH\Scripts\Activate.ps1"

if (Test-Path $ACTIVATE_SCRIPT) {
    Write-Host "Activating State of Decay 2 AI Environment..." -ForegroundColor Cyan
    . $ACTIVATE_SCRIPT
} else {
    Write-Host "Error: Activation script not found at $ACTIVATE_SCRIPT." -ForegroundColor Red
}