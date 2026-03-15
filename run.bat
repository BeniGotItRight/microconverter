@echo off
REM Convertex - Start the file converter app (Windows)
cd /d "%~dp0"

where python >nul 2>&1
if errorlevel 1 (
    where py >nul 2>&1
    if errorlevel 1 (
        echo Error: Python not found. Install Python from https://python.org
        pause
        exit /b 1
    )
    set PY=py
) else (
    set PY=python
)

if not exist ".venv" (
    echo Creating virtual environment...
    %PY% -m venv .venv
)
call .venv\Scripts\activate.bat
pip install -q -r requirements.txt 2>nul || pip install -r requirements.txt

echo.
echo Starting Convertex...
echo   Local:   http://localhost:8501
echo   Network: http://YOUR_IP:8501 (replace YOUR_IP with your machine's IP)
echo.

streamlit run app.py --server.headless=true --server.port=8501
