# WallpaperChanger - Configuration Guide

## Overview
WallpaperChanger uses a flexible configuration system that supports both `.env` files and `config.json` files, providing backward compatibility and advanced configuration options.

## 📁 Configuration Files

| File | Purpose | Format | When to Use |
|------|---------|--------|-------------|
| `.env` | Environment variables and API keys | KEY=value format | Simple setup, API keys |
| `config.json` | Advanced application settings | JSON format | Complex configuration |
| `.env.example` | Template for .env file | Template | Initial setup |
| `config.template.json` | Template for JSON config | Template | Initial setup |

## 🚀 Quick Setup

### Method 1: Interactive Setup (Recommended)
```cmd
python setup_config.py
```
This will guide you through the entire configuration process interactively.

### Method 2: Minimal Setup
```cmd
python setup_config.py --minimal
```
Creates a basic configuration using Reddit (no API keys required).

### Method 3: Manual Setup
1. Copy `.env.example` to `.env`
2. Copy `config.template.json` to `config.json`
3. Edit the files with your settings

## 🔑 API Keys Configuration

### Required API Keys

#### Wallhaven
- **URL**: https://wallhaven.cc/settings/account
- **Purpose**: High-quality wallpapers from Wallhaven.cc
- **Required**: Yes, for Wallhaven provider
- **Rate Limit**: 45 requests per minute

#### Pexels
- **URL**: https://www.pexels.com/api/new/
- **Purpose**: Professional stock photos
- **Required**: Yes, for Pexels provider
- **Rate Limit**: 200 requests per hour

### Optional API Keys

#### Unsplash
- **URL**: https://unsplash.com/developers
- **Purpose**: Beautiful photography
- **Required**: Optional
- **Rate Limit**: 50 requests per hour

#### Pixabay
- **URL**: https://pixabay.com/api/docs/
- **Purpose**: Free images and videos
- **Required**: Optional
- **Rate Limit**: 100 requests per hour

#### Google Gemini (AI Features)
- **URL**: https://makersuite.google.com/app/apikey
- **Purpose**: AI-powered features (mood detection, recommendations)
- **Required**: Optional, for AI features
- **Rate Limit**: 15 requests per minute (free tier)

#### OpenWeatherMap (Weather Integration)
- **URL**: https://openweathermap.org/api
- **Purpose**: Weather-based wallpaper selection
- **Required**: Optional, for weather features
- **Rate Limit**: 1000 calls per day (free tier)

## 📄 .env File Format

```bash
# ========================================
# Wallpaper Provider API Keys
# ========================================

WALLHAVEN_API_KEY=your_wallhaven_api_key_here
PEXELS_API_KEY=your_pexels_api_key_here
UNSPLASH_ACCESS_KEY=your_unsplash_access_key_here
PIXABAY_API_KEY=your_pixabay_api_key_here

# ========================================
# AI Services API Keys
# ========================================

GEMINI_API_KEY=your_gemini_api_key_here
OPENAI_API_KEY=your_openai_api_key_here

# ========================================
# Weather Integration
# ========================================

OPENWEATHER_API_KEY=your_openweather_api_key_here

# ========================================
# Application Settings
# ========================================

DEFAULT_PROVIDER=reddit
ENABLE_PROVIDER_ROTATION=true
PROVIDER_SEQUENCE=wallhaven,pexels,reddit
PEXELS_MODE=curated
PEXELS_QUERY=nature
```

## 📋 config.json Format

```json
{
  "api_keys": {
    "wallhaven": {
      "key": "your_wallhaven_api_key_here",
      "description": "Get your API key from https://wallhaven.cc/settings/account",
      "required": true,
      "provider": "wallhaven"
    },
    "pexels": {
      "key": "your_pexels_api_key_here",
      "description": "Get your API key from https://www.pexels.com/api/new/",
      "required": true,
      "provider": "pexels"
    }
  },
  "providers": {
    "default": "reddit",
    "rotation_enabled": true,
    "rotation_sequence": ["wallhaven", "pexels", "reddit"],
    "wallhaven": {
      "enabled": true,
      "categories": ["general", "anime", "people"],
      "purity": ["sfw"],
      "sorting": "random",
      "resolutions": ["1920x1080", "2560x1440", "3840x2160"]
    },
    "pexels": {
      "enabled": true,
      "mode": "curated",
      "search_query": "nature",
      "orientation": "landscape"
    },
    "reddit": {
      "enabled": true,
      "subreddits": ["wallpapers", "wallpaper", "EarthPorn"],
      "sort": "hot",
      "limit": 60
    }
  },
  "application": {
    "auto_rotate": true,
    "change_interval_minutes": 30,
    "start_minimized": false,
    "enable_system_tray": true
  }
}
```

## 🖼️ Provider Configuration

### Wallhaven Settings
- **categories**: `["general", "anime", "people"]`
- **purity**: `["sfw", "sketchy", "nsfw"]`
- **sorting**: `["random", "toplist", "favorites", "views"]`
- **top_range**: `["1d", "3d", "1w", "1m", "3m", "6m", "1y"]`
- **resolutions**: Array of preferred resolutions

### Pexels Settings
- **mode**: `"search"` or `"curated"`
- **search_query**: Search term when using search mode
- **orientation**: `"landscape"`, `"portrait"`, `"square"`
- **size**: `"small"`, `"medium"`, `"large"`
- **color**: Color filter or `null` for any

### Reddit Settings
- **subreddits**: Array of subreddit names
- **sort**: `"hot"`, `"new"`, `"rising"`, `"top"`, `"controversial"`
- **time_filter**: `"hour"`, `"day"`, `"week"`, `"month"`, `"year"`, `"all"`
- **limit**: Maximum number of wallpapers to fetch

## 🔧 Configuration Manager API

### Using in Python

```python
from config_manager import get_config_manager

# Get configuration manager instance
config = get_config_manager()

# Get API key
wallhaven_key = config.get_api_key('wallhaven')

# Get provider configuration
wallhaven_config = config.get_provider_config('wallhaven')

# Check if provider is enabled
if config.is_provider_enabled('pexels'):
    # Use Pexels provider
    pass

# Get default provider
default = config.get_default_provider()

# Update configuration
config.update_json_value('providers.wallhaven.enabled', False)

# Validate API keys
validation = config.validate_api_keys()
```

### Environment Variable Access

```python
# Get environment variable with type casting
value = config.get_env('SOME_SETTING', 'default_value', bool)

# Supported types: str, int, float, bool, list
```

### JSON Configuration Access

```python
# Get nested value using dot notation
value = config.get_json('providers.wallhaven.categories', ['general'])

# Update nested value
config.update_json_value('application.change_interval_minutes', 60)
```

## 🎯 Best Practices

### 1. Security
- Never commit `.env` file to version control
- Use strong, unique API keys
- Rotate API keys regularly
- Use read-only API keys when possible

### 2. Performance
- Enable provider rotation for variety
- Set appropriate cache limits
- Use reasonable request intervals
- Choose optimal resolution for your display

### 3. Reliability
- Configure multiple providers
- Set up proper error handling
- Monitor API rate limits
- Use Reddit as fallback (no API key required)

### 4. Organization
- Keep API keys in `.env` file
- Use `config.json` for application settings
- Document custom configurations
- Backup configuration files

## 🛠️ Troubleshooting

### Common Issues

#### API Key Not Working
1. Verify key is copied correctly (no extra spaces)
2. Check if key is active in provider dashboard
3. Ensure you haven't exceeded rate limits
4. Try regenerating the API key

#### Configuration Not Loading
1. Check file permissions
2. Validate JSON syntax
3. Ensure files are in correct directory
4. Check for encoding issues

#### Provider Not Working
1. Verify API key is set
2. Check provider is enabled in config
3. Test API key with provider's documentation
4. Check network connectivity

### Debug Mode

Enable debug mode in configuration:
```json
{
  "application": {
    "debug_mode": true,
    "logging": {
      "level": "DEBUG"
    }
  }
}
```

Or via environment variable:
```bash
DEBUG_MODE=true python main.py
```

### Configuration Validation

Run configuration validation:
```python
from config_manager import get_config_manager

config = get_config_manager()
summary = config.get_config_summary()
print(summary)
```

## 📚 Advanced Configuration

### Custom Provider Settings

```json
{
  "providers": {
    "custom_provider": {
      "enabled": true,
      "api_endpoint": "https://api.example.com/wallpapers",
      "api_key_param": "api_key",
      "response_format": "json",
      "image_url_field": "url",
      "pagination": {
        "page_param": "page",
        "limit_param": "limit"
      }
    }
  }
}
```

### Multi-Monitor Configuration

```json
{
  "monitors": {
    "multi_monitor_support": true,
    "span_mode": false,
    "per_monitor_settings": {
      "1": {
        "enabled": true,
        "provider": "wallhaven",
        "filters": {
          "categories": ["nature"]
        }
      },
      "2": {
        "enabled": true,
        "provider": "pexels",
        "filters": {
          "search_query": "abstract"
        }
      }
    }
  }
}
```

### AI Features Configuration

```json
{
  "ai_features": {
    "enabled": true,
    "mood_detection": true,
    "smart_recommendations": true,
    "auto_categorization": true,
    "color_analysis": true,
    "provider": "gemini",
    "cache_analysis": true
  }
}
```

## 🔄 Migration Guide

### From Old Configuration
1. Run `python setup_config.py`
2. Choose to overwrite existing files
3. Re-enter API keys
4. Verify provider settings

### Backup and Restore
```bash
# Backup configuration
cp .env .env.backup
cp config.json config.json.backup

# Restore configuration
cp .env.backup .env
cp config.json.backup config.json
```

This configuration system provides maximum flexibility while maintaining backward compatibility and ease of use.
