@echo off
setlocal

set "MODE=%~1"
if "%MODE%"=="" set "MODE=both"

if /I not "%MODE%"=="claude" if /I not "%MODE%"=="cursor" if /I not "%MODE%"=="both" (
  echo.
  echo Usage: scripts\run_agentic_ai.bat [claude^|cursor^|both]
  echo Example: scripts\run_agentic_ai.bat both
  exit /b 1
)

echo.
echo [Agentic AI] Starting setup for mode: %MODE%
echo [Agentic AI] Running bootstrap checks...
powershell -ExecutionPolicy Bypass -File "scripts\bootstrap_agentic_qa.ps1"
if errorlevel 1 (
  echo [Agentic AI] Bootstrap failed. Fix errors above and retry.
  exit /b 1
)

if /I "%MODE%"=="claude" goto :claude
if /I "%MODE%"=="cursor" goto :cursor
if /I "%MODE%"=="both" goto :both

:claude
echo.
echo [Claude] Use these project files:
echo   - .claude\settings.json
echo   - .claude\hooks\
echo   - .claude\commands\
echo   - .claude\AGENTIC_QA_GUIDE.md
echo.
echo [Claude] Suggested next command:
echo   pytest -m "TC6 or TC7" -q
goto :end

:cursor
echo.
echo [Cursor] Use these project files:
echo   - .cursor\hooks.json
echo   - .cursor\mcp.json
echo   - .cursor\rules\
echo   - .cursor\AGENTIC_QA_GUIDE.md
echo.
echo [Cursor] Suggested next command:
echo   pytest -m "TC6 or TC7" -q
goto :end

:both
echo.
echo [Claude + Cursor] Project is ready for both modes.
echo.
echo Claude files:
echo   - .claude\settings.json
echo   - .claude\AGENTIC_QA_GUIDE.md
echo.
echo Cursor files:
echo   - .cursor\hooks.json
echo   - .cursor\mcp.json
echo   - .cursor\AGENTIC_QA_GUIDE.md
echo.
echo Suggested next commands:
echo   pytest --collect-only -q
echo   pytest -m "TC6 or TC7" -q
goto :end

:end
echo.
echo [Agentic AI] Done.
exit /b 0
