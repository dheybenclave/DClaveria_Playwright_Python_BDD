param(
    [string]$PythonExe = "python",
    [switch]$InstallBrowsers = $true,
    [switch]$RunSmokeCollect = $true
)

$ErrorActionPreference = "Stop"

Write-Host "[Agentic QA] Bootstrap starting..." -ForegroundColor Cyan

Write-Host "[1/5] Python version"
& $PythonExe --version

Write-Host "[2/5] Install Python dependencies"
& $PythonExe -m pip install --upgrade pip
& $PythonExe -m pip install -r requirements.txt

if ($InstallBrowsers) {
    Write-Host "[3/5] Install Playwright browsers"
    try {
        & $PythonExe -m playwright install --with-deps
    }
    catch {
        Write-Host "[Agentic QA] Fallback to playwright install (without --with-deps)"
        & $PythonExe -m playwright install
    }
}
else {
    Write-Host "[3/5] Skipped browser install"
}

Write-Host "[4/5] Verify project environment"
& $PythonExe .cursor/skills/init/scripts/verify_env.py

if ($RunSmokeCollect) {
    Write-Host "[5/5] Run smoke collection"
    & $PythonExe .cursor/skills/init/scripts/smoke_collect.py
}
else {
    Write-Host "[5/5] Skipped smoke collect"
}

Write-Host "[Agentic QA] Bootstrap complete." -ForegroundColor Green
Write-Host "Next: pytest -m `"TC6 or TC7`" -q"
