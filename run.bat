@echo off
echo ============================================================
echo 🎬 AI Video Generator - Windows Launcher
echo ============================================================
echo.

echo Starting AI Video Generator...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Error: Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://python.org
    pause
    exit /b 1
)

REM Run the setup script
echo 📦 Setting up dependencies...
python setup.py

if errorlevel 1 (
    echo ❌ Setup failed. Please check the error messages above.
    pause
    exit /b 1
)

echo.
echo ✅ Setup completed! Starting the application...
echo.
echo 🌐 Frontend: http://localhost:3000
echo 🔧 Backend:  http://localhost:8000
echo.
echo Press Ctrl+C to stop the servers
echo.

REM Start both servers
python setup.py --run

pause
