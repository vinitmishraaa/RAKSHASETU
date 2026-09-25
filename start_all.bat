@echo off
title RakshaSetu Launcher
echo ======================================================================
echo       RAKSHASETU (रक्षासेतु) - NATIONAL DISASTER DECISION PLATFORM
echo       Ministry of Home Affairs / National Disaster Response Force
echo    Decision Support System for Red Zones ^& Relocation Needs
echo ======================================================================
echo.

set ROOT_DIR=%~dp0

echo [1/2] Starting Backend FastAPI Server on http://127.0.0.1:8000 ...
start "RakshaSetu Backend (FastAPI)" cmd /k "cd /d ""%ROOT_DIR%backend"" && ""%ROOT_DIR%venv\Scripts\python.exe"" -m uvicorn app.main:app --reload --port 8000"

timeout /t 3 /nobreak >nul

echo [2/2] Starting Frontend Vite Server on http://localhost:5173 ...
start "RakshaSetu Frontend (React + Vite)" cmd /k "cd /d ""%ROOT_DIR%frontend"" && npm run dev"

timeout /t 3 /nobreak >nul

echo.
echo Launching RakshaSetu in your default browser...
start http://localhost:5173

echo.
echo ======================================================================
echo RakshaSetu is running successfully!
echo - Frontend UI:  http://localhost:5173
echo - Backend API:  http://127.0.0.1:8000
echo - Swagger Docs: http://127.0.0.1:8000/docs
echo.
echo You can keep this terminal open or minimize it.
echo To stop the servers, simply close the respective backend/frontend command windows.
echo ======================================================================
pause >nul
