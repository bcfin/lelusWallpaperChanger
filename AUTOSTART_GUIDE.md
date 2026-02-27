# WallpaperChanger - Autostart Configuration Guide

## Overview
WallpaperChanger can be configured to start automatically when Windows boots up. The autostart functionality has been completely rewritten with robust path handling and error checking.

## 🔧 **New Features**

### Robust Path Handling
- ✅ Handles paths with spaces and special characters
- ✅ Uses proper quoting throughout
- ✅ Works from any directory location
- ✅ Validates file existence before setup

### Dual Autostart Methods
- **Registry Entry**: `HKEY_CURRENT_USER\SOFTWARE\Microsoft\Windows\CurrentVersion\Run`
- **Startup Folder**: `%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\`

### Comprehensive Error Handling
- ✅ Pre-flight checks for required files
- ✅ Detailed logging for troubleshooting
- ✅ User-friendly error messages
- ✅ Graceful fallback handling

## 📁 **Files Created**

| File | Purpose | Features |
|------|---------|----------|
| `setup_autostart.vbs` | Enable autostart | Registry + Startup folder, logging, validation |
| `uninstall_autostart.vbs` | Disable autostart | Complete removal, verification |
| `AUTOSTART.bat` | Manual management | Simple CLI interface, status checking |
| `autostart_setup.log` | Setup logs | Detailed troubleshooting information |
| `autostart_uninstall.log` | Uninstall logs | Removal verification details |

## 🚀 **Usage Methods**

### Method 1: During Installation (Recommended)
1. Run `INSTALL.bat`
2. Choose "Y" when asked about autostart
3. Automatic setup with both registry and startup folder

### Method 2: Manual Setup
```cmd
cscript.exe //nologo setup_autostart.vbs
```

### Method 3: Batch Interface
```cmd
AUTOSTART.bat
```
- Shows current status
- Enable/disable options
- User-friendly menu

### Method 4: Manual Removal
```cmd
cscript.exe //nologo uninstall_autostart.vbs
```

## 🔍 **What Gets Configured**

### Registry Entry
```
Key: HKEY_CURRENT_USER\SOFTWARE\Microsoft\Windows\CurrentVersion\Run
Name: WallpaperChanger
Value: wscript.exe "C:\path\to\run_hidden_enhanced.vbs"
```

### Startup Folder Shortcut
```
Location: %APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\
File: WallpaperChanger.lnk
Target: wscript.exe "C:\path\to\run_hidden_enhanced.vbs"
```

## 📋 **Verification**

### Check Registry Entry
```cmd
reg query "HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Run" /v "WallpaperChanger"
```

### Check Startup Folder
```cmd
dir "%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\WallpaperChanger.lnk"
```

### Use Status Tool
```cmd
AUTOSTART.bat
```

## 🛠️ **Troubleshooting**

### Autostart Not Working
1. **Check logs**: `autostart_setup.log` for setup errors
2. **Verify files**: Ensure `run_hidden_enhanced.vbs` exists
3. **Check permissions**: Run installer as administrator if needed
4. **Test manually**: Run `run_hidden_enhanced.vbs` directly

### Common Issues
| Issue | Cause | Solution |
|-------|-------|----------|
| "File not found" | Missing `run_hidden_enhanced.vbs` | Reinstall or copy file |
| "Access denied" | Insufficient permissions | Run as administrator |
| "Path too long" | Deep directory nesting | Move to shorter path |
| "Registry error" | Registry protection | Check antivirus settings |

## 🔄 **Integration with Uninstaller**

The `UNINSTALL.bat` now includes automatic autostart removal:
- Detects and removes registry entries
- Deletes startup folder shortcuts
- Falls back to manual removal if scripts missing
- Preserves user settings and cache

## 📊 **Technical Details**

### Path Quoting Strategy
- VBScript uses triple quotes: `"""path with spaces"""`
- Batch files use proper variable expansion: `"%SCRIPT_DIR%file.vbs"`
- PowerShell commands escape quotes correctly: `\"path\"`

### Error Recovery
- Registry failures don't prevent startup folder setup
- Startup folder failures don't prevent registry setup
- At least one method ensures autostart functionality
- Detailed logging for post-mortem analysis

### Security Considerations
- Uses HKEY_CURRENT_USER (no admin rights required)
- Scripts are signed with clear descriptions
- No network access during startup
- Validates file paths before execution

## 🎯 **Best Practices**

1. **Use Enhanced Launcher**: `run_hidden_enhanced.vbs` provides logging
2. **Check Logs First**: Always review `autostart_setup.log` for issues
3. **Test After Setup**: Verify autostart works before relying on it
4. **Keep Scripts**: Don't delete `.vbs` files after setup
5. **Update After Moving**: Run setup again if moving the application

## 🆕 **Improvements Over Old System**

| Old System | New System |
|------------|------------|
| Single method (startup folder) | Dual methods (registry + startup) |
| Basic path handling | Robust quoting for all paths |
| No error checking | Comprehensive validation |
| No logging | Detailed troubleshooting logs |
| Manual removal only | Automated uninstall |
| PowerShell dependency | Pure VBScript (more reliable) |

The new autostart system is production-ready and handles edge cases that previously caused failures.
