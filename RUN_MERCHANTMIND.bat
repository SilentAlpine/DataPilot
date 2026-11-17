@echo off
setlocal
cd /d "%~dp0"
echo ================================================
echo           DataPilot - LAUNCHER
echo ================================================
where py >nul 2>nul
if %errorlevel%==0 (
    set PY=py
) else (
    where python >nul 2>nul
    if errorlevel 1 (
        echo Python was not found. Install Python 3.10-3.12 and try again.
        pause
        exit /b 1
    )
    set PY=python
)
if not exist ".venv\Scripts\python.exe" (
    echo Creating virtual environment...
    %PY% -m venv .venv
)
echo Installing or checking required packages...
.venv\Scripts\python.exe -m pip install --upgrade pip
.venv\Scripts\python.exe -m pip install -r requirements.txt
if errorlevel 1 (
    echo Package installation failed. Check your internet connection and Python installation.
    pause
    exit /b 1
)
echo Starting DataPilot...
.venv\Scripts\python.exe -m streamlit run app.py
pause
