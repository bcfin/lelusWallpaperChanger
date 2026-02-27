@echo off
REM WallpaperChanger - Hidden Background Launcher
REM This batch file runs the VBScript to start main.py in the background

cd /d "%~dp0"

REM Check if the VBScript exists
if not exist "run_hidden.vbs" (
    echo ERROR: run_hidden.vbs not found!
    echo.
    pause
    exit /b 1
)

REM Run the VBScript launcher
cscript.exe //nologo run_hidden.vbs

REM Exit immediately (no pause to keep it hidden)
exit /b 0
