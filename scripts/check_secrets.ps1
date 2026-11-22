# scripts/check_secrets.ps1
# CodeBridge — Scan git-tracked files for accidentally committed secrets
# Usage: .\scripts\check_secrets.ps1
#
# Checks for:
#   - "AIza..."        — Gemini / Google API key prefix
#   - "GOOGLE_API_KEY=A" — inline key assignment
#   - Generic patterns: long hex/base64 tokens in known variable names
#
# Skips: .env files, .gitignore, binary files, the scripts directory itself

$ErrorActionPreference = "Stop"

Write-Host ""
Write-Host "============================================" -ForegroundColor Cyan
Write-Host "  CodeBridge — Secret Scanner" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

# ── Resolve project root (parent of scripts/) ─────────────────────────────────
$projectRoot = Resolve-Path "$PSScriptRoot\.."

# ── Collect git-tracked files ─────────────────────────────────────────────────
Push-Location $projectRoot
try {
    $trackedFiles = git ls-files 2>$null
} catch {
    Write-Host "[WARN] 'git ls-files' failed — not a git repo or git not installed." -ForegroundColor Yellow
    Write-Host "       Falling back to scanning all text files in project root." -ForegroundColor Yellow
    $trackedFiles = Get-ChildItem -Recurse -File | Where-Object {
        $_.Extension -match '\.(py|ts|tsx|js|json|md|txt|toml|yaml|yml|ps1|sh|env\.example)$'
    } | Resolve-Path -Relative
}
Pop-Location

# ── Patterns to flag ──────────────────────────────────────────────────────────
$patterns = @(
    'AIza[0-9A-Za-z\-_]{35}',       # Google/Gemini API key
    'GOOGLE_API_KEY\s*=\s*[A-Za-z0-9]',  # Inline env assignment with a value
    'api[_\-]?key\s*=\s*["\047][A-Za-z0-9]{20,}',  # Generic api_key = "..."
    'secret\s*=\s*["\047][A-Za-z0-9]{16,}'          # Generic secret = "..."
)

# ── Files / paths to skip ─────────────────────────────────────────────────────
$skipPatterns = @(
    '\.env$',
    '\.env\.',       # .env.example etc (they should only have placeholders)
    '\.gitignore$',
    'check_secrets\.ps1$',  # This script itself references the patterns
    '\.png$', '\.jpg$', '\.ico$', '\.woff', '\.ttf$'  # Binaries
)

function Should-Skip ($path) {
    foreach ($p in $skipPatterns) {
        if ($path -match $p) { return $true }
    }
    return $false
}

# ── Scan ──────────────────────────────────────────────────────────────────────
$failures = @()

foreach ($relPath in $trackedFiles) {
    if ([string]::IsNullOrWhiteSpace($relPath)) { continue }
    if (Should-Skip $relPath) { continue }

    $fullPath = Join-Path $projectRoot $relPath

    if (-not (Test-Path $fullPath -PathType Leaf)) { continue }

    try {
        $content = Get-Content $fullPath -Raw -Encoding UTF8 -ErrorAction SilentlyContinue
    } catch {
        continue  # skip unreadable / binary
    }
    if ($null -eq $content) { continue }

    foreach ($pat in $patterns) {
        if ($content -match $pat) {
            $failures += [PSCustomObject]@{
                File    = $relPath
                Pattern = $pat
            }
            break  # one match per file is enough to flag it
        }
    }
}

# ── Report ────────────────────────────────────────────────────────────────────
if ($failures.Count -eq 0) {
    Write-Host "[PASS] No secret patterns found in git-tracked files." -ForegroundColor Green
    Write-Host ""
    exit 0
} else {
    Write-Host "[FAIL] Potential secrets detected in the following files:" -ForegroundColor Red
    Write-Host ""
    foreach ($f in $failures) {
        Write-Host "  File   : $($f.File)" -ForegroundColor Yellow
        Write-Host "  Pattern: $($f.Pattern)" -ForegroundColor DarkYellow
        Write-Host ""
    }
    Write-Host "ACTION: Remove these values, rotate the affected keys, and re-commit." -ForegroundColor Red
    Write-Host "        Ensure your .env file is listed in .gitignore." -ForegroundColor Red
    Write-Host ""
    exit 1
}
