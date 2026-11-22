# scripts/run_dev.ps1
# CodeBridge — Launch backend and frontend dev servers (Windows)
# Usage: .\scripts\run_dev.ps1

$ErrorActionPreference = "Stop"

$projectRoot = Resolve-Path "$PSScriptRoot\.."
$backendDir  = Join-Path $projectRoot "backend"
$frontendDir = Join-Path $projectRoot "frontend"
$envFile1    = Join-Path $backendDir ".env"
$envFile2    = Join-Path $projectRoot ".env"

Write-Host ""
Write-Host "============================================" -ForegroundColor Cyan
Write-Host "  CodeBridge — Dev Server Launcher" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

# ── 1. Check for .env ─────────────────────────────────────────────────────────
if (-not (Test-Path $envFile1) -and -not (Test-Path $envFile2)) {
    Write-Host "[WARN] No .env file found in backend/ or project root." -ForegroundColor Yellow
    Write-Host "       Creating backend\.env from template..." -ForegroundColor DarkGray
    Copy-Item (Join-Path $projectRoot ".env.example") $envFile1 -Force
    Write-Host "[ACTION REQUIRED] Please edit backend\.env and add your GOOGLE_API_KEY." -ForegroundColor Yellow
    Write-Host ""
} else {
    Write-Host "[OK] Environment file found." -ForegroundColor Green
}

# ── 2. Locate Python binary ───────────────────────────────────────────────────
$pythonCmd = "python"
$candidatePy = "C:\Users\DELL\AppData\Local\Programs\Python\Python313\python.exe"
if (Test-Path $candidatePy) {
    $pythonCmd = "& '$candidatePy'"
}

# ── 3. Start backend ──────────────────────────────────────────────────────────
Write-Host "[...] Starting FastAPI backend (port 8000)..." -ForegroundColor Cyan
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$backendDir'; $pythonCmd -m uvicorn main:app --reload --port 8000"

# ── 4. Wait for backend to initialise ────────────────────────────────────────
Write-Host "[...] Waiting 3 seconds for backend to start..." -ForegroundColor DarkGray
Start-Sleep -Seconds 3

# ── 5. Start frontend ─────────────────────────────────────────────────────────
Write-Host "[...] Starting Vite frontend (port 5173)..." -ForegroundColor Cyan
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$frontendDir'; npm run dev"

# ── 6. Print URLs ─────────────────────────────────────────────────────────────
Write-Host ""
Write-Host "--------------------------------------------" -ForegroundColor DarkGray
Write-Host "  Frontend: http://localhost:5173" -ForegroundColor Green
Write-Host "  Backend:  http://localhost:8000" -ForegroundColor Green
Write-Host "  API Docs: http://localhost:8000/docs" -ForegroundColor Green
Write-Host "--------------------------------------------" -ForegroundColor DarkGray
Write-Host ""
Write-Host "Both servers are launching in separate windows." -ForegroundColor White
Write-Host "If you already built the frontend, http://localhost:8000 also serves the full app!" -ForegroundColor Cyan
Write-Host ""
