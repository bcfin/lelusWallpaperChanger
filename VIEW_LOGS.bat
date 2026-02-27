@echo off
REM WallpaperChanger - Log Viewer Launcher
REM Easy access to debug logs and error analysis

cd /d "%~dp0"

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo Python is not installed or not in PATH
    echo.
    echo Please run INSTALL.bat first, or install Python from:
    echo https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)

REM Show menu
cls
echo ========================================
echo   WallpaperChanger - Log Viewer
echo ========================================
echo.
echo 1. View recent debug logs (last 50 lines)
echo 2. View error summary
echo 3. Search logs
echo 4. Show log statistics
echo 5. Clear logs
echo 6. Monitor logs live (tail)
echo 7. Open log files in notepad
echo 8. Exit
echo.

choice /C 12345678 /M "Select option"

if errorlevel 8 (
    exit /b 0
)
if errorlevel 7 (
    echo Opening log files in notepad...
    start notepad debug.log
    if exist error.log start notepad error.log
)
if errorlevel 6 (
    echo Monitoring debug logs (Press Ctrl+C to stop)...
    python view_logs.py tail --type debug
)
if errorlevel 5 (
    echo.
    echo Select which logs to clear:
    echo 1. Debug logs only
    echo 2. Error logs only
    echo 3. All logs
    echo.
    choice /C 123 /M "Clear option"
    if errorlevel 3 (
        python view_logs.py clear --clear-type all
    )
    if errorlevel 2 (
        python view_logs.py clear --clear-type error
    )
    if errorlevel 1 (
        python view_logs.py clear --clear-type debug
    )
)
if errorlevel 4 (
    python view_logs.py stats
)
if errorlevel 3 (
    set /p pattern="Enter search pattern: "
    if "!pattern!" neq "" (
        python view_logs.py search --pattern "!pattern!"
    ) else (
        echo No pattern provided.
    )
)
if errorlevel 2 (
    python view_logs.py errors
)
if errorlevel 1 (
    python view_logs.py recent --lines 50
)

echo.
pause
