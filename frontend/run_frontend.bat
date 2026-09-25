@echo off
title RakshaSetu Frontend (React + Vite)
cd /d "%~dp0"
echo ======================================================================
echo Starting RakshaSetu Vite Frontend Server...
echo ======================================================================
echo Frontend UI URL: http://localhost:5173
echo.

call npm run dev
if %ERRORLEVEL% neq 0 (
    echo.
    echo ======================================================================
    echo [ERROR] Frontend failed to start (Exit code: %ERRORLEVEL%).
    echo ======================================================================
    pause
)
