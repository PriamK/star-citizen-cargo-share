@echo off
REM ========================================
REM Star Citizen Cargo Share - Build Script
REM ========================================

echo.
echo ╔═══════════════════════════════════════════════════════════╗
echo ║   ⬢ STAR CITIZEN CARGO SHARE - BUILD EXECUTABLE ⬢       ║
echo ╚═══════════════════════════════════════════════════════════╝
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH
    echo Please install Python 3.7+ from https://www.python.org/
    pause
    exit /b 1
)

echo [1/4] Installing PyInstaller...
pip install pyinstaller>=6.0.0

echo.
echo [2/4] Cleaning previous builds...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist

echo.
echo [3/4] Building executable with PyInstaller...
pyinstaller cargo-share.spec

echo.
echo [4/4] Build complete!
echo.

if exist "dist\StarCitizenCargoShare.exe" (
    echo ╔═══════════════════════════════════════════════════════════╗
    echo ║                    ✓ BUILD SUCCESSFUL                     ║
    echo ╚═══════════════════════════════════════════════════════════╝
    echo.
    echo Executable location: dist\StarCitizenCargoShare.exe
    echo.
) else (
    echo ╔═══════════════════════════════════════════════════════════╗
    echo ║                    ✗ BUILD FAILED                         ║
    echo ╚═══════════════════════════════════════════════════════════╝
    echo.
    echo Please check the error messages above.
    echo.
)

pause
