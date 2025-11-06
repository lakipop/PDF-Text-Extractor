@echo off
REM Change to the directory where this batch file is located
cd /d "%~dp0"

echo ========================================
echo PDF Text Extractor - Running
echo ========================================
echo.

REM Check if virtual environment exists
if not exist venv (
    echo [ERROR] Virtual environment not found!
    echo Please run SETUP.bat first.
    pause
    exit /b 1
)

REM Check if .env exists
if not exist .env (
    echo [ERROR] .env file not found!
    echo Please run SETUP.bat first and configure your settings.
    pause
    exit /b 1
)

REM Activate virtual environment and run the Python script
call venv\Scripts\activate.bat
python process_pdfs.py

if errorlevel 1 (
    echo.
    echo [ERROR] Script execution failed!
    echo Check processing.log for details.
    if "%TERM_PROGRAM%"=="" pause
    exit /b 1
)

echo.
echo ========================================
echo Processing Complete!
echo ========================================
echo Check extracted_notes.md for results
echo.

REM Only pause if run from double-click (not from terminal)
if "%TERM_PROGRAM%"=="" pause
