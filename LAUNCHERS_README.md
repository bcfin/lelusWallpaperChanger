# WallpaperChanger - Background Launchers

## Overview
These launchers allow you to run WallpaperChanger in the background without visible command prompt windows.

## Files Created

### 1. `run_hidden.vbs`
**Basic VBScript launcher**
- Runs `main.py` using `pythonw.exe` in the background
- No visible command prompt window
- Minimal error checking

### 2. `run_hidden_enhanced.vbs`
**Enhanced VBScript launcher with logging**
- Comprehensive error handling
- Creates log file (`wallpaper_changer_launcher.log`)
- Checks Python availability
- Validates requirements installation
- Detailed error messages

### 3. `RUN_HIDDEN.bat`
**Batch file wrapper**
- Calls the basic VBScript launcher
- Easy to double-click
- Quick validation

## Usage Methods

### Method 1: Direct VBScript (Recommended)
```cmd
wscript.exe run_hidden.vbs
```
Or for enhanced version with logging:
```cmd
wscript.exe run_hidden_enhanced.vbs
```

### Method 2: Batch File
```cmd
RUN_HIDDEN.bat
```

### Method 3: Start Menu Shortcut
After running `INSTALL.bat`, use:
- Start Menu → Wallpaper Changer → "Start Background Service"

## Features

### Basic Launcher (`run_hidden.vbs`)
- ✅ Hidden execution (no console window)
- ✅ Validates `main.py` exists
- ✅ Uses `pythonw.exe` for background execution
- ⚠️ Minimal error handling

### Enhanced Launcher (`run_hidden_enhanced.vbs`)
- ✅ All basic features
- ✅ Python availability check
- ✅ Requirements validation
- ✅ Detailed logging to `wallpaper_changer_launcher.log`
- ✅ User-friendly error messages
- ✅ Timestamped log entries

## Log File Location
The enhanced launcher creates logs at:
```
WallpaperChanger\wallpaper_changer_launcher.log
```

## Troubleshooting

### If WallpaperChanger doesn't start:
1. Check the log file (enhanced launcher)
2. Ensure Python is installed and in PATH
3. Run `INSTALL.bat` to install dependencies
4. Verify `main.py` exists in the same directory

### Common Issues:
- **"Python not found"** → Install Python or add to PATH
- **"main.py not found"** → Ensure you're in the correct directory
- **"Requirements missing"** → Run `INSTALL.bat`

## Integration with System

### Autostart Setup
The installer can configure WallpaperChanger to start automatically:
- Run `INSTALL.bat`
- Choose "Y" when asked about autostart
- Uses enhanced launcher for reliability

### System Tray
When running in background, WallpaperChanger appears in the system tray for easy access to settings and controls.

## Security Notes
- VBScript files are safe to run
- They only execute Python scripts in the same directory
- No network access or system modifications beyond wallpaper changes

## Comparison

| Feature | Basic | Enhanced |
|---------|--------|----------|
| Hidden execution | ✅ | ✅ |
| Error checking | Basic | Comprehensive |
| Logging | ❌ | ✅ |
| Python validation | ❌ | ✅ |
| Requirements check | ❌ | ✅ |
| User-friendly errors | ❌ | ✅ |

**Recommendation**: Use the enhanced launcher (`run_hidden_enhanced.vbs`) for production use.
