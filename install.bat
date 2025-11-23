@echo off
REM Simple installation script for ImageEffectGen (Windows)

echo ==========================================
echo ImageEffectGen - Installation
echo ==========================================
echo.

REM Check Python
echo Checking Python version...
python --version
if errorlevel 1 (
    echo Error: Python is not installed!
    pause
    exit /b 1
)
echo.

REM Check pip
echo Checking pip...
pip --version
if errorlevel 1 (
    echo Error: pip is not installed!
    pause
    exit /b 1
)
echo.

REM Install dependencies
echo Installing dependencies...
echo This may take a few minutes...
echo.
pip install -r requirements.txt

if errorlevel 0 (
    echo.
    echo ==========================================
    echo Installation Complete!
    echo ==========================================
    echo.
    echo Next steps:
    echo   1. Run demo:          python demo.py
    echo   2. Use with image:    python run_filter.py your_image.jpg
    echo   3. See quick guide:   type QUICKSTART.md
    echo.
) else (
    echo.
    echo Installation failed!
    echo Try running manually: pip install -r requirements.txt
)

pause
