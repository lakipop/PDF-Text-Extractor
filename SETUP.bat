@echo off
echo ========================================
echo PDF Text Extractor - Setup
echo ========================================
echo.

echo [1/3] Checking Python installation...
python --version
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH!
    echo Please install Python 3.8 or higher from python.org
    pause
    exit /b 1
)

echo.
echo [2/3] Installing required packages...
python -m pip install --upgrade pip
pip install -r requirements.txt

if errorlevel 1 (
    echo [ERROR] Failed to install dependencies!
    pause
    exit /b 1
)

echo.
echo [3/3] Creating environment file...
if not exist .env (
    copy .env.example .env
    echo [INFO] Created .env file from template
    echo [ACTION REQUIRED] Please edit .env and add your Azure credentials!
) else (
    echo [INFO] .env file already exists
)

echo.
echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo Next steps:
echo 1. Edit .env file with your Azure credentials
echo 2. Place PDF files in the configured folder
echo 3. Run RUN.bat to start processing
echo.
pause
