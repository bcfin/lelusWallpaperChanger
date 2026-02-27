# WallpaperChanger - Logging System Guide

## Overview
WallpaperChanger includes a comprehensive logging system that writes detailed debug information to log files in the application folder, making troubleshooting easy without needing to run the application via terminal.

## 📁 Log Files

| File | Purpose | Content | Rotation |
|------|---------|----------|-----------|
| `debug.log` | General application logs | 10MB max, 5 backups |
| `error.log` | Error-specific logs | 5MB max, 3 backups |
| `crash_report_*.txt` | Crash reports | Created on fatal errors |

### Log Location
```
WallpaperChanger/
├── debug.log          # Main application logs
├── error.log          # Error-only logs
├── debug.log.1       # Rotated backup
├── debug.log.2       # Rotated backup
└── crash_report_*.txt # Crash reports
```

## 🔧 Configuration

### Environment Variables
```bash
# Set logging level
LOG_LEVEL=DEBUG          # DEBUG, INFO, WARNING, ERROR, CRITICAL

# Enable console output (when running from terminal)
DEBUG_CONSOLE=true
```

### Log Levels
- **DEBUG**: Detailed debugging information, function calls, API requests
- **INFO**: General information, wallpaper changes, configuration updates
- **WARNING**: Non-critical issues that don't stop the application
- **ERROR**: Errors that may affect functionality
- **CRITICAL**: Fatal errors that crash the application

## 📊 Log Format

### Standard Log Entry
```
2024-02-27 12:30:45 | INFO     | main               | change_wallpaper      :856 | Changing wallpaper (trigger: startup)
```

**Format Breakdown:**
- `Timestamp`: `YYYY-MM-DD HH:MM:SS`
- `Level`: Log level (8 characters, aligned)
- `Logger`: Module/function name (15 characters, aligned)
- `Function`: Function name and line number
- `Message`: Log message

### Special Log Entries

#### Wallpaper Changes
```
WALLPAPER_CHANGED [startup] reddit: /path/to/wallpaper.jpg
```

#### API Requests
```
API Request [wallhaven] https://wallhaven.cc/api/v1/search -> 200
```

#### Configuration Changes
```
CONFIG_CHANGED default_provider: 'reddit' -> 'wallhaven'
```

## 🛠️ Log Management Tools

### 1. View Logs Utility
```cmd
# Show recent logs
python view_logs.py recent --lines 100

# Show error summary
python view_logs.py errors

# Search logs
python view_logs.py search --pattern "wallpaper"

# Show statistics
python view_logs.py stats

# Monitor logs live
python view_logs.py tail

# Clear logs
python view_logs.py clear --clear-type debug
```

### 2. Batch File Interface
```cmd
# Interactive menu
VIEW_LOGS.bat
```

Provides easy access to:
- Recent log viewing
- Error analysis
- Log searching
- Statistics
- Log clearing
- Live monitoring
- Opening logs in notepad

### 3. Direct File Access
```cmd
# Open in notepad
notepad debug.log
notepad error.log

# Open in text editor of choice
code debug.log
```

## 🔍 Troubleshooting Guide

### Common Issues and Solutions

#### Application Won't Start
**Check logs for:**
```
ERROR | Failed to import module: xxx
CRITICAL | Fatal error in main: xxx
```

**Solutions:**
- Missing dependencies → Run `INSTALL.bat`
- Python version issues → Check Python 3.13+ compatibility
- Configuration errors → Check `.env` and `config.json`

#### Wallpaper Not Changing
**Check logs for:**
```
ERROR | Failed to set wallpaper: xxx
INFO | No wallpapers found from provider: xxx
API Request [wallhaven] https://... -> 401
```

**Solutions:**
- API key issues → Check API key configuration
- Network problems → Check internet connection
- File permissions → Check write permissions

#### API Rate Limiting
**Check logs for:**
```
WARNING | Rate limit exceeded for provider: wallhaven
ERROR | HTTP 429: Too Many Requests
```

**Solutions:**
- Increase change interval
- Use multiple providers with rotation
- Check API quota limits

#### Memory/Performance Issues
**Check logs for:**
```
WARNING | High memory usage: xxx MB
DEBUG | Cache cleanup started
ERROR | Out of memory
```

**Solutions:**
- Reduce cache size
- Lower concurrent downloads
- Check system resources

## 📈 Log Analysis

### Error Patterns
Look for recurring error patterns:

#### Connection Issues
```
ERROR | Connection timeout: xxx
ERROR | DNS resolution failed: xxx
WARNING | Retrying connection (attempt 3/5)
```

#### File System Issues
```
ERROR | Permission denied: xxx
ERROR | Disk space insufficient
WARNING | File locked: xxx
```

#### API Issues
```
ERROR | HTTP 401: Unauthorized
ERROR | HTTP 403: Forbidden
ERROR | HTTP 429: Rate Limited
```

### Performance Monitoring
Monitor these metrics:

#### Startup Performance
```
INFO | Initializing WallpaperApp
INFO | Cache loaded in 1.2 seconds
INFO | All providers initialized in 0.8 seconds
```

#### Wallpaper Change Performance
```
INFO | Wallpaper downloaded in 2.1 seconds
INFO | Wallpaper processed in 0.5 seconds
INFO | Wallpaper set successfully
```

## 🚨 Crash Reports

When a fatal error occurs, a crash report is automatically generated:

### Crash Report Contents
```
============================================================
WALLPAPER CHANGER CRASH REPORT
============================================================
Timestamp: 2024-02-27T12:30:45.123456
Context: main.change_wallpaper
Python Version: 3.13.0 (main, Oct 24 2024, 00:00:00)
Working Directory: C:\WallpaperChanger

CONTEXT:
Changing wallpaper from Reddit provider

EXCEPTION:
Traceback (most recent call last):
  File "main.py", line 856, in change_wallpaper
    wallpapers = self.fetch_from_provider(...)
  File "main.py", line 1234, in fetch_from_reddit
    response = requests.get(url, timeout=30)
  ...

SYSTEM INFO:
OS: Windows 11 22H31
Architecture: AMD64
Processor: Intel64 Family 6 Model 158 Stepping 10
============================================================
```

### Using Crash Reports
1. **Identify the Error**: Look at the exception type and message
2. **Find Context**: Understand what the application was doing
3. **Check System Info**: Verify OS and Python compatibility
4. **Search Solutions**: Use error message to find solutions
5. **Report Issues**: Include crash report when reporting bugs

## 🔧 Advanced Configuration

### Custom Log Formatting
```python
from logger_config import setup_logging, get_logger

# Setup with custom level
setup_logging(log_level='DEBUG')

# Get module-specific logger
logger = get_logger('my_module')
logger.info("Custom log message")
```

### Log Filtering
```python
# Filter by level
import logging
logger.setLevel(logging.WARNING)  # Only WARNING and above

# Filter by module
module_logger = get_logger('api_requests')
```

### Performance Logging
```python
from logger_config import log_function_calls

@log_function_calls('api')
def fetch_wallpapers():
    # Automatically logs function entry/exit
    pass
```

## 📋 Best Practices

### For Users
1. **Check Logs First**: Always check `debug.log` before reporting issues
2. **Use Error Summary**: Run `python view_logs.py errors` for quick analysis
3. **Monitor Live Logs**: Use `python view_logs.py tail` to see real-time activity
4. **Clear Old Logs**: Periodically clear logs to save disk space
5. **Save Crash Reports**: Keep crash reports for bug reporting

### For Developers
1. **Use Appropriate Levels**: DEBUG for development, INFO for production
2. **Log Context**: Include relevant context in log messages
3. **Avoid Sensitive Data**: Don't log API keys or passwords
4. **Use Structured Messages**: Follow consistent log message format
5. **Handle Exceptions**: Always log exceptions with full context

## 🎯 Quick Reference

### Common Log Commands
```cmd
# Quick error check
python view_logs.py errors

# Recent activity
python view_logs.py recent --lines 20

# Search for specific provider
python view_logs.py search --pattern "wallhaven"

# Live monitoring
python view_logs.py tail

# Clear old logs
python view_logs.py clear --clear-type all
```

### Log File Locations
- **Main Log**: `debug.log`
- **Error Log**: `error.log`
- **Crash Reports**: `crash_report_YYYYMMDD_HHMMSS.txt`

This logging system provides comprehensive visibility into application behavior, making troubleshooting and debugging much easier without requiring terminal access.
