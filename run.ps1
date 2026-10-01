# Start the FastAPI backend and Next.js frontend together on Windows.
#
# Usage: ./run.ps1
# Stop: press Ctrl+C. The backend process is stopped automatically.

$ErrorActionPreference = "Stop"
Set-Location -Path $PSScriptRoot

if (-not (Test-Path -LiteralPath "frontend/node_modules")) {
    throw "Frontend dependencies are missing. Run 'npm --prefix frontend install' first."
}

Write-Host "Starting FastAPI backend on http://localhost:8000 ..." -ForegroundColor Cyan
$backend = Start-Process -PassThru -FilePath "python" `
    -ArgumentList "-m", "uvicorn", "backend.api:app", "--port", "8000" `
    -WindowStyle Hidden

Start-Sleep -Seconds 2

try {
    Write-Host "Starting Glance on http://localhost:3000 ..." -ForegroundColor Cyan
    npm --prefix frontend run dev
}
finally {
    Write-Host "Shutting down backend (PID $($backend.Id)) ..." -ForegroundColor Yellow
    if (-not $backend.HasExited) { Stop-Process -Id $backend.Id -Force }
}
