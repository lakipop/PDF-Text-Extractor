@echo off
echo ========================================
echo PDF Text Extractor - Running
echo ========================================
echo.

REM Check if .env exists
if not exist .env (
    echo [ERROR] .env file not found!
    echo Please run SETUP.bat first and configure your settings.
    pause
    exit /b 1
)

REM Run the Python script
python process_pdfs.py

if errorlevel 1 (
    echo.
    echo [ERROR] Script execution failed!
    echo Check processing.log for details.
    pause
    exit /b 1
)

echo.
echo ========================================
echo Processing Complete!
echo ========================================
echo Check extracted_notes.md for results
echo.
pause
