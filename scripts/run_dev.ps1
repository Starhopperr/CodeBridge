# scripts/run_dev.ps1
# CodeBridge — Launch backend and frontend dev servers (Windows)
# Usage: .\scripts\run_dev.ps1

$ErrorActionPreference = "Stop"

$projectRoot = Resolve-Path "$PSScriptRoot\.."
$backendDir  = Join-Path $projectRoot "backend"
$frontendDir = Join-Path $projectRoot "frontend"
$envFile     = Join-Path $backendDir ".env"

Write-Host ""
Write-Host "============================================" -ForegroundColor Cyan
Write-Host "  CodeBridge — Dev Server Launcher" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

# ── 1. Check for backend .env ─────────────────────────────────────────────────
if (-not (Test-Path $envFile)) {
    Write-Host "[ERROR] backend\.env not found." -ForegroundColor Red
    Write-Host "        Copy backend\.env.example to backend\.env and add your GOOGLE_API_KEY." -ForegroundColor Yellow
    Write-Host ""
    exit 1
}
Write-Host "[OK] backend\.env found." -ForegroundColor Green

# ── 2. Start backend ──────────────────────────────────────────────────────────
Write-Host "[...] Starting backend (FastAPI / uvicorn)..." -ForegroundColor Cyan
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$backendDir'; uvicorn main:app --reload"

# ── 3. Wait for backend to initialise ────────────────────────────────────────
Write-Host "[...] Waiting 3 seconds for backend to initialise..." -ForegroundColor DarkGray
Start-Sleep -Seconds 3

# ── 4. Start frontend ─────────────────────────────────────────────────────────
Write-Host "[...] Starting frontend (Vite / React)..." -ForegroundColor Cyan
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$frontendDir'; npm run dev"

# ── 5. Print URLs ─────────────────────────────────────────────────────────────
Write-Host ""
Write-Host "--------------------------------------------" -ForegroundColor DarkGray
Write-Host "  Backend:  http://localhost:8000" -ForegroundColor Green
Write-Host "  Frontend: http://localhost:5173" -ForegroundColor Green
Write-Host "  API Docs: http://localhost:8000/docs" -ForegroundColor Green
Write-Host "--------------------------------------------" -ForegroundColor DarkGray
Write-Host ""
Write-Host "Both servers are running in separate windows." -ForegroundColor White
Write-Host "Close those windows (or press Ctrl+C in each) to stop them." -ForegroundColor DarkGray
Write-Host ""
