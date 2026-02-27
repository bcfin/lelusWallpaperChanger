# WallpaperChanger - Complete User Guide

## 📋 Table of Contents
1. [Quick Start](#quick-start)
2. [First-Time Setup](#first-time-setup)
3. [Configuration After Installation](#configuration-after-installation)
4. [Daily Usage](#daily-usage)
5. [Troubleshooting](#troubleshooting)
6. [Advanced Features](#advanced-features)

---

## 🚀 Quick Start

### For Immediate Use (No API Keys Required)
```cmd
# 1. Install dependencies
INSTALL.bat

# 2. Start with Reddit (no API key needed)
START.bat

# 3. Or run hidden in background
RUN_HIDDEN.bat
```

### For Full Features (API Keys Required)
```cmd
# 1. Install dependencies
INSTALL.bat

# 2. Configure API keys
python setup_config.py

# 3. Start application
START.bat
```

---

## 🎯 First-Time Setup

### Step 1: Installation

#### Method A: Automated Installation (Recommended)
```cmd
# Run the installer
INSTALL.bat
```

**What this does:**
- ✅ Installs all required Python packages
- ✅ Creates desktop shortcut
- ✅ Sets up autostart (optional)
- ✅ Creates configuration templates
- ✅ Verifies installation

#### Method B: Manual Installation
```cmd
# Install Python packages
pip install -r requirements.txt

# Create configuration files
copy .env.example .env
copy config.template.json config.json

# Run configuration wizard
python setup_config.py
```

### Step 2: Initial Configuration

#### Option A: Interactive Configuration Wizard (Recommended)
```cmd
python setup_config.py
```

**Wizard Features:**
- 🎯 **Guided Setup**: Step-by-step configuration
- 🔑 **API Key Setup**: Easy API key entry for all providers
- 🖼️ **Provider Selection**: Choose which wallpaper sources to use
- ⚙️ **Basic Settings**: Configure change intervals and preferences
- ✅ **Validation**: Checks API keys and settings

**Wizard Walkthrough:**

1. **Existing Configuration Check**
   ```
   🔍 Checking existing configuration...
   ✅ .env file found: C:\WallpaperChanger\.env
   ❌ config.json not found: C:\WallpaperChanger\config.json
   ```

2. **Template Creation**
   ```
   📝 Creating config.json from template...
   ✅ config.json created successfully
   ```

3. **API Key Setup**
   ```
   🔑 API Key Setup
   ------------------------------
   
   Wallhaven API Key ❌ Missing
   Get your key at: https://wallhaven.cc/settings/account
   Enter API key (or press Enter to skip): your_api_key_here
   ✅ Wallhaven API key saved
   ```

4. **Provider Configuration**
   ```
   🖼️ Provider Configuration
   ------------------------------
   Current default provider: reddit
   Provider rotation: Enabled
   Rotation sequence: wallhaven, pexels, reddit
   
   Default provider [reddit]: wallhaven
   Enable provider rotation? [Y]: Y
   ```

#### Option B: Minimal Setup (Reddit Only)
```cmd
python setup_config.py --minimal
```

**Perfect for:**
- 🚀 Quick testing
- 🔧 Initial setup
- 📱 Users who don't want API keys
- ⚡ Immediate functionality

#### Option C: Manual Configuration

1. **Edit .env file**
   ```cmd
   notepad .env
   ```
   
   Add your API keys:
   ```bash
   # Required for full functionality
   WALLHAVEN_API_KEY=your_wallhaven_api_key_here
   PEXELS_API_KEY=your_pexels_api_key_here
   
   # Optional providers
   UNSPLASH_ACCESS_KEY=your_unsplash_key_here
   PIXABAY_API_KEY=your_pixabay_key_here
   ```

2. **Edit config.json**
   ```cmd
   notepad config.json
   ```
   
   Configure providers:
   ```json
   {
     "providers": {
       "default": "wallhaven",
       "rotation_enabled": true,
       "wallhaven": {
         "enabled": true,
         "categories": ["general", "anime", "people"],
         "purity": ["sfw"],
         "sorting": "random"
       }
     },
     "application": {
       "auto_rotate": true,
       "change_interval_minutes": 30
     }
   }
   ```

### Step 3: First Launch

#### Method A: Normal Launch
```cmd
START.bat
```
- Opens GUI interface
- Shows system tray icon
- Allows manual wallpaper changes

#### Method B: Hidden Launch
```cmd
RUN_HIDDEN.bat
```
- Runs in background
- No visible window
- System tray only
- Perfect for autostart

#### Method C: GUI Configuration
```cmd
python gui_config.py
```
- Full configuration interface
- API key management
- Provider settings
- Advanced options

---

## ⚙️ Configuration After Installation

### Accessing Configuration

#### Method 1: GUI Configuration (Recommended)
```cmd
python gui_config.py
```

**Features:**
- 🎨 Visual interface
- 🔑 API key management
- 🖼️ Provider configuration
- ⚙️ Application settings
- 📊 Statistics viewing

#### Method 2: Configuration Files
```cmd
# Environment variables and API keys
notepad .env

# Advanced configuration
notepad config.json
```

#### Method 3: Configuration Wizard
```cmd
python setup_config.py
```

### Essential Configuration Options

#### 1. Wallpaper Providers

**Reddit (No API Key Required)**
```json
"reddit": {
  "enabled": true,
  "subreddits": ["wallpapers", "wallpaper", "EarthPorn"],
  "sort": "hot",
  "limit": 60
}
```

**Wallhaven (API Key Required)**
```json
"wallhaven": {
  "enabled": true,
  "categories": ["general", "anime", "people"],
  "purity": ["sfw"],
  "sorting": "random",
  "resolutions": ["1920x1080", "2560x1440"]
}
```

**Pexels (API Key Required)**
```json
"pexels": {
  "enabled": true,
  "mode": "curated",
  "search_query": "nature",
  "orientation": "landscape"
}
```

#### 2. Application Settings

**Basic Settings**
```json
"application": {
  "auto_rotate": true,
  "change_interval_minutes": 30,
  "start_minimized": false,
  "enable_system_tray": true
}
```

**Advanced Settings**
```json
"application": {
  "cache_settings": {
    "max_size_mb": 500,
    "cleanup_days": 30
  },
  "download_settings": {
    "timeout_seconds": 30,
    "max_concurrent": 3
  }
}
```

#### 3. API Key Management

**Via GUI**
1. Open `python gui_config.py`
2. Navigate to "API Keys" tab
3. Enter your keys
4. Click "Save"

**Via Configuration Files**
```bash
# .env file
WALLHAVEN_API_KEY=your_key_here
PEXELS_API_KEY=your_key_here
UNSPLASH_ACCESS_KEY=your_key_here
```

**Getting API Keys:**

| Provider | URL | Cost | Rate Limit |
|----------|-----|------|------------|
| Wallhaven | https://wallhaven.cc/settings/account | Free | 45/min |
| Pexels | https://www.pexels.com/api/new/ | Free | 200/hour |
| Unsplash | https://unsplash.com/developers | Free | 50/hour |
| Pixabay | https://pixabay.com/api/docs/ | Free | 100/hour |

### Common Configuration Scenarios

#### Scenario 1: Minimal Setup (Reddit Only)
```cmd
python setup_config.py --minimal
```

**Result:**
- ✅ Works immediately
- 🔑 No API keys needed
- 🖼️ Reddit wallpapers only
- ⚡ Fast setup

#### Scenario 2: Balanced Setup (2-3 Providers)
```json
{
  "providers": {
    "default": "wallhaven",
    "rotation_enabled": true,
    "rotation_sequence": ["wallhaven", "pexels", "reddit"],
    "wallhaven": {"enabled": true},
    "pexels": {"enabled": true},
    "reddit": {"enabled": true}
  }
}
```

**Result:**
- 🎨 High variety
- 🔑 2 API keys needed
- 🔄 Automatic rotation
- ⚖️ Good balance

#### Scenario 3: Maximum Variety (All Providers)
```json
{
  "providers": {
    "default": "wallhaven",
    "rotation_enabled": true,
    "rotation_sequence": ["wallhaven", "pexels", "unsplash", "pixabay", "reddit"],
    "wallhaven": {"enabled": true},
    "pexels": {"enabled": true},
    "unsplash": {"enabled": true},
    "pixabay": {"enabled": true},
    "reddit": {"enabled": true}
  }
}
```

**Result:**
- 🎨 Maximum variety
- 🔑 4 API keys needed
- 🔄 Full rotation
- 🌟 Best experience

---

## 📱 Daily Usage

### Basic Operations

#### Manual Wallpaper Change
1. **Right-click system tray icon**
2. **Select "Change Wallpaper"**
3. **Choose provider (optional)**
4. **Wallpaper updates immediately**

#### Using GUI
```cmd
python gui_config.py
```

**Main Features:**
- 🖼️ **Preview**: See next wallpapers
- ⏭️ **Skip**: Skip to next wallpaper
- ⭐ **Favorite**: Mark wallpapers as favorites
- 📊 **Stats**: View usage statistics

#### Keyboard Shortcuts
- `Ctrl+Alt+W`: Change wallpaper
- `Ctrl+Alt+S`: Skip to next
- `Ctrl+Alt+F`: Favorite current
- `Ctrl+Alt+Q`: Quit application

### System Tray Features

**Right-Click Menu:**
- 🖼️ Change Wallpaper
- ⏭️ Skip to Next
- ⭐ Favorite Current
- 📊 View Statistics
- ⚙️ Configuration
- 📋 About
- ❌ Exit

**Left-Click:**
- Quick wallpaper change
- Show current wallpaper info

### Monitoring and Logs

#### Check Recent Activity
```cmd
VIEW_LOGS.bat
# Option 1: View recent debug logs
```

#### Error Troubleshooting
```cmd
VIEW_LOGS.bat
# Option 2: View error summary
```

#### Live Monitoring
```cmd
python view_logs.py tail
```

---

## 🔧 Troubleshooting

### Common Issues and Solutions

#### Issue 1: Application Won't Start
**Symptoms:**
- Error window on launch
- No system tray icon
- Command window flashes and closes

**Solutions:**
1. **Check Dependencies**
   ```cmd
   INSTALL.bat
   ```

2. **Check Logs**
   ```cmd
   VIEW_LOGS.bat
   # Option 2: View error summary
   ```

3. **Verify Python Installation**
   ```cmd
   python --version
   # Should show Python 3.13+
   ```

#### Issue 2: Wallpaper Not Changing
**Symptoms:**
- System tray icon present but no changes
- Manual change doesn't work
- Same wallpaper stays

**Solutions:**
1. **Check API Keys**
   ```cmd
   python gui_config.py
   # Check API Keys tab
   ```

2. **Check Provider Status**
   ```cmd
   python view_logs.py search --pattern "API Request"
   ```

3. **Test Different Provider**
   ```cmd
   python gui_config.py
   # Try Reddit (no API key needed)
   ```

#### Issue 3: High CPU/Memory Usage
**Symptoms:**
- System running slowly
- High memory usage
- Frequent disk activity

**Solutions:**
1. **Adjust Cache Settings**
   ```json
   "cache_settings": {
     "max_size_mb": 200,
     "cleanup_days": 7
   }
   ```

2. **Increase Change Interval**
   ```json
   "change_interval_minutes": 60
   ```

3. **Disable Unused Providers**
   ```json
   "unsplash": {"enabled": false},
   "pixabay": {"enabled": false}
   ```

#### Issue 4: Network/Connection Problems
**Symptoms:**
- "Connection timeout" errors
- "DNS resolution failed"
- No wallpapers downloading

**Solutions:**
1. **Check Internet Connection**
   ```cmd
   ping google.com
   ```

2. **Increase Timeout**
   ```json
   "download_settings": {
     "timeout_seconds": 60
   }
   ```

3. **Check Firewall/Antivirus**
   - Allow WallpaperChanger through firewall
   - Add exception for Python

### Getting Help

#### 1. Check Logs First
```cmd
VIEW_LOGS.bat
# Always check logs before reporting issues
```

#### 2. Create Crash Report
If application crashes:
1. Look for `crash_report_*.txt` files
2. Include in bug reports
3. Note what you were doing when it crashed

#### 3. System Information
Include in bug reports:
- Windows version
- Python version
- Error messages
- Configuration (remove API keys)

---

## 🌟 Advanced Features

### 1. Provider Rotation

**Setup Automatic Rotation**
```json
{
  "providers": {
    "rotation_enabled": true,
    "rotation_sequence": ["wallhaven", "pexels", "reddit"],
    "rotation_mode": "sequential"  // or "random"
  }
}
```

**Benefits:**
- 🎨 Maximum variety
- 🔄 Automatic switching
- ⚖️ Load balancing
- 🌟 Fresh content

### 2. Weather-Based Wallpapers

**Setup Weather Integration**
```json
{
  "weather_integration": {
    "enabled": true,
    "api_key": "your_openweather_key",
    "location": "New York, US",
    "mappings": {
      "clear": ["sunny", "bright"],
      "cloudy": ["overcast", "moody"],
      "rainy": ["rain", "water"]
    }
  }
}
```

### 3. AI-Powered Features

**Setup AI Integration**
```json
{
  "ai_features": {
    "enabled": true,
    "provider": "gemini",
    "mood_detection": true,
    "smart_recommendations": true,
    "auto_categorization": true
  }
}
```

**Features:**
- 🧠 Mood-based selection
- 🎯 Smart recommendations
- 🏷️ Automatic categorization
- 🎨 Color analysis

### 4. Multi-Monitor Support

**Setup Multiple Monitors**
```json
{
  "monitors": {
    "multi_monitor_support": true,
    "span_mode": false,
    "per_monitor_settings": {
      "1": {
        "enabled": true,
        "provider": "wallhaven",
        "filters": {"categories": ["nature"]}
      },
      "2": {
        "enabled": true,
        "provider": "pexels",
        "filters": {"search_query": "abstract"}
      }
    }
  }
}
```

### 5. Presets and Playlists

**Create Presets**
```cmd
python gui_config.py
# Go to Presets tab
# Create new preset with specific settings
```

**Benefits:**
- 🎭 Different moods/themes
- ⏰ Time-based switching
- 🏠 Work vs home settings
- 🌙 Day vs night modes

### 6. Statistics and Analytics

**View Usage Statistics**
```cmd
python gui_config.py
# Go to Statistics tab
```

**Available Stats:**
- 📊 Most used providers
- ⏱️ Average change time
- 🖼️ Total wallpapers downloaded
- ⭐ Favorite wallpapers
- 📈 Usage trends

---

## 📚 Quick Reference

### Essential Commands
```cmd
# Installation
INSTALL.bat                    # Install dependencies and setup

# Launch
START.bat                      # Normal launch with GUI
RUN_HIDDEN.bat                 # Hidden launch (background only)
python gui_config.py           # Configuration interface

# Configuration
python setup_config.py         # Interactive setup wizard
python setup_config.py --minimal  # Quick Reddit-only setup

# Logs and Troubleshooting
VIEW_LOGS.bat                  # Interactive log viewer
python view_logs.py recent     # View recent logs
python view_logs.py errors      # Error analysis
```

### File Locations
```
WallpaperChanger/
├── .env                       # API keys and environment vars
├── config.json               # Advanced configuration
├── debug.log                 # Application logs
├── error.log                 # Error-only logs
├── wallpaper_stats.json      # Usage statistics
└── cache/                    # Downloaded wallpapers
```

### Configuration Priority
1. **Environment Variables** (`.env`) - API keys, basic settings
2. **JSON Configuration** (`config.json`) - Advanced settings
3. **GUI Settings** - Runtime preferences
4. **Defaults** - Fallback values

### Common Tasks

| Task | Command | Notes |
|------|--------|-------|
| Install | `INSTALL.bat` | Run once |
| Quick Setup | `python setup_config.py --minimal` | Reddit only |
| Full Setup | `python setup_config.py` | All providers |
| Configure | `python gui_config.py` | Visual interface |
| Troubleshoot | `VIEW_LOGS.bat` | Check errors first |
| Update API Keys | `python gui_config.py` → API Keys tab | Secure storage |

---

## 🎯 Best Practices

### For New Users
1. **Start with minimal setup** (`--minimal`)
2. **Test Reddit provider first** (no API key)
3. **Add API keys gradually** (one at a time)
4. **Check logs if issues occur**
5. **Use GUI for easy configuration**

### For Power Users
1. **Configure multiple providers**
2. **Enable provider rotation**
3. **Set up weather integration**
4. **Create presets for different moods**
5. **Monitor statistics and optimize**

### For System Administrators
1. **Use silent installation**
2. **Deploy configuration files**
3. **Set up centralized logging**
4. **Monitor resource usage**
5. **Plan backup and recovery**

---

## 📞 Support and Resources

### Documentation
- `README_USER.md` - Basic overview
- `CONFIGURATION_GUIDE.md` - Detailed configuration
- `LOGGING_GUIDE.md` - Troubleshooting and logs
- `AI_FEATURES.md` - AI-powered features

### Community
- GitHub Issues: Report bugs and request features
- Wiki: Community guides and tutorials
- Discussions: Tips and tricks from other users

### Getting Help
1. **Check this guide first**
2. **Review logs** (`VIEW_LOGS.bat`)
3. **Search existing issues**
4. **Create detailed bug report** with:
   - System information
   - Error messages
   - Configuration (remove API keys)
   - Steps to reproduce

---

## 🎉 Conclusion

WallpaperChanger is designed to be both powerful and user-friendly. Whether you want a simple set-and-forget solution or a highly customized wallpaper experience, this guide should help you get the most out of the application.

**Remember:**
- 🚀 Start simple, add complexity gradually
- 🔑 API keys unlock the best features
- 📊 Logs are your best troubleshooting tool
- 🎨 Experiment with different providers and settings
- 🌟 Have fun discovering beautiful wallpapers!

Enjoy your dynamic wallpaper experience! 🖼️✨
