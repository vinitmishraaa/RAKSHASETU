@echo off
title RakshaSetu Backend (FastAPI)
cd /d "%~dp0"
echo ======================================================================
echo Starting RakshaSetu FastAPI Backend Server...
echo ======================================================================

set "PYTHON_EXE="
if exist "%~dp0..\venv\Scripts\python.exe" (
    set "PYTHON_EXE=%~dp0..\venv\Scripts\python.exe"
) else if exist "%~dp0venv\Scripts\python.exe" (
    set "PYTHON_EXE=%~dp0venv\Scripts\python.exe"
) else if exist "%~dp0.venv\Scripts\python.exe" (
    set "PYTHON_EXE=%~dp0.venv\Scripts\python.exe"
) else (
    set "PYTHON_EXE=python"
)

echo Python Interpreter: %PYTHON_EXE%
echo Backend API URL:    http://127.0.0.1:8000
echo Interactive Docs:   http://127.0.0.1:8000/docs
echo.

"%PYTHON_EXE%" -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
if %ERRORLEVEL% neq 0 (
    echo.
    echo ======================================================================
    echo [ERROR] Backend failed to start (Exit code: %ERRORLEVEL%).
    echo If port 8000 is in use, please close other instances.
    echo ======================================================================
    pause
)
