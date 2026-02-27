@echo off
REM WallpaperChanger - Autostart Manager
REM Simple interface to enable/disable autostart

cd /d "%~dp0"
cls

echo ========================================
echo   WallpaperChanger - Autostart Manager
echo ========================================
echo.
echo Current Status:
echo.

REM Check current autostart status
reg query "HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Run" /v "WallpaperChanger" >nul 2>&1
if %errorlevel% == 0 (
    echo [ENABLED] Registry entry found
    set REG_STATUS=enabled
) else (
    echo [DISABLED] No registry entry
    set REG_STATUS=disabled
)

if exist "%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\WallpaperChanger.lnk" (
    echo [ENABLED] Startup folder shortcut found
    set STARTUP_STATUS=enabled
) else (
    echo [DISABLED] No startup folder shortcut
    set STARTUP_STATUS=disabled
)

echo.
echo Options:
echo   1. Enable Autostart
echo   2. Disable Autostart
echo   3. Exit
echo.

choice /C 123 /M "Select option"

if errorlevel 3 (
    exit /b 0
)
if errorlevel 2 (
    echo.
    echo Disabling autostart...
    if exist "uninstall_autostart.vbs" (
        cscript.exe //nologo uninstall_autostart.vbs
    ) else (
        echo ERROR: uninstall_autostart.vbs not found!
    )
    pause
    exit /b 0
)
if errorlevel 1 (
    echo.
    echo Enabling autostart...
    if exist "setup_autostart.vbs" (
        cscript.exe //nologo setup_autostart.vbs
    ) else (
        echo ERROR: setup_autostart.vbs not found!
    )
    pause
    exit /b 0
)
