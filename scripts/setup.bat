@echo off
REM SmartScreen SaaS - Startup Script for Windows

echo =========================================
echo   SmartScreen SaaS - Developer Startup
echo =========================================
echo.

REM Check Python
echo Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo X Python not found
    exit /b 1
)
echo OK - Python found

REM Check Node
echo Checking Node.js installation...
node --version >nul 2>&1
if not errorlevel 1 (
    echo OK - Node.js found
) else (
    echo WARNING - Node.js not found (needed for frontend)
)

echo.
echo =========================================
echo   Backend Setup
echo =========================================

REM Create virtual environment if it doesn't exist
if not exist "venv" (
    echo Creating Python virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo Installing backend dependencies...
pip install -r requirements.txt -q

REM Create .env if it doesn't exist
if not exist "backend\.env" (
    echo Creating .env file from template...
    copy .env.example backend\.env
    echo WARNING - Edit backend\.env with your configuration
)

echo.
echo =========================================
echo   Frontend Setup
echo =========================================

if exist "frontend" (
    cd frontend
    
    if not exist "node_modules" (
        echo Installing frontend dependencies...
        call npm install
    )
    
    REM Create .env for frontend
    if not exist ".env" (
        echo Creating frontend .env...
        copy .env.example .env
    )
    
    cd ..
)

echo.
echo =========================================
echo   OK - Setup Complete!
echo =========================================
echo.
echo To start development, run in separate terminals:
echo.
echo Terminal 1 - Backend:
echo   cd backend
echo   set PYTHONPATH=.
echo   uvicorn main:app --reload --host 0.0.0.0 --port 8000
echo.
echo Terminal 2 - Frontend:
echo   cd frontend
echo   npm start
echo.
echo Then open: http://localhost:3000
echo API Docs:  http://localhost:8000/docs
echo.
echo For more info, see:
echo   - README_NEW.md
echo   - QUICK_REFERENCE.md
echo   - BACKEND_SETUP.md
echo.
pause
