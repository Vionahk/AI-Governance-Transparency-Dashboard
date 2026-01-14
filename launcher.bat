@echo off
setlocal enabledelayedexpansion
cls

echo.
echo ===============================================================================
echo  AI Governance and Transparency Dashboard Launcher
echo ===============================================================================
echo.
echo Current directory: %CD%
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python not found!
    echo Please install Python 3.10 or higher
    pause
    endlocal
    exit /b 1
)

echo [OK] Python is installed
echo.

REM Check if app.py exists
if not exist app.py (
    echo ERROR: app.py not found!
    echo Current directory: %CD%
    echo.
    pause
    endlocal
    exit /b 1
)

echo [OK] Running from correct directory
echo.

REM Create virtual environment if needed
if not exist venv (
    echo [1/4] Creating virtual environment...
    python -m venv venv
    if %errorlevel% neq 0 (
        echo ERROR: Failed to create virtual environment
        pause
        endlocal
        exit /b 1
    )
    echo [OK] Virtual environment created
    echo.
)

REM Activate virtual environment
call venv\Scripts\activate.bat
if %errorlevel% neq 0 (
    echo ERROR: Failed to activate virtual environment
    pause
    endlocal
    exit /b 1
)

REM Upgrade pip and tools
echo [2/4] Ensuring pip is up to date...
python -m pip install --upgrade pip setuptools wheel >nul 2>&1

REM Install dependencies
echo [3/4] Installing dependencies...
echo.
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ERROR: Failed to install dependencies
    pause
    endlocal
    exit /b 1
)
echo [OK] Dependencies installed
echo.

REM Check if models exist and train if needed
if not exist models\model_metadata.json (
    echo [4/4] Training models - this may take 2-3 minutes...
    echo.
    python train_models.py
    if %errorlevel% neq 0 (
        echo ERROR: Model training failed
        pause
        endlocal
        exit /b 1
    )
    echo [OK] Models trained successfully
    echo.
) else (
    echo [4/4] Models already trained - skipping training
    echo.
)

echo ===============================================================================
echo  Starting Streamlit Dashboard
echo ===============================================================================
echo.
echo  Dashboard URL: http://localhost:8501
echo.
echo  Press Ctrl+C to stop the server
echo ===============================================================================
echo.

python -m streamlit run app.py

endlocal
exit /b 0
