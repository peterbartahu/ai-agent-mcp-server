@echo off
REM Quick Start Script for AI Study Helper Agent (Windows)
REM This script creates venv if needed, installs dependencies, starts MongoDB, and runs the server

echo.
echo Starting AI Study Helper Agent...
echo.

REM Check if Docker is available
docker --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Docker is not installed or not in PATH
    echo Please install Docker Desktop and try again
    pause
    exit /b 1
)

REM Check and create venv if it doesn't exist
if not exist "venv" (
    echo [1/4] Creating Python virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo ERROR: Failed to create virtual environment
        pause
        exit /b 1
    )
    echo     [OK] Virtual environment created
) else (
    echo [1/4] Virtual environment already exists
)

echo.
echo [2/4] Activating virtual environment...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo ERROR: Failed to activate virtual environment
    pause
    exit /b 1
)

REM Check if dependencies are installed
python -c "import fastapi" >nul 2>&1
if errorlevel 1 (
    echo [3/4] Installing dependencies...
    python -m pip install --upgrade pip -q
    python -m pip install fastapi uvicorn pymongo python-dotenv -q
    if errorlevel 1 (
        echo ERROR: Failed to install dependencies
        pause
        exit /b 1
    )
    echo     [OK] Dependencies installed
) else (
    echo [3/4] Dependencies already installed
)

echo.
echo [4/4] Starting MongoDB...
docker-compose up -d >nul 2>&1
if errorlevel 1 (
    echo ERROR: Failed to start MongoDB with docker-compose
    echo Make sure Docker Desktop is running
    pause
    exit /b 1
)
timeout /t 2 /nobreak >nul
echo     [OK] MongoDB started

echo.
echo Starting FastAPI server...
echo.
echo Server will run on: http://localhost:8000
echo Swagger UI:        http://localhost:8000/docs
echo API Docs:          http://localhost:8000/redoc
echo.
echo Press Ctrl+C to stop the server
echo.

REM Start the server
python -m uvicorn app.web:app --reload --host 0.0.0.0 --port 8000

pause
