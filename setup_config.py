#!/usr/bin/env python3
"""
WallpaperChanger Configuration Setup Utility
Helps users create initial configuration files and set up API keys
"""

import os
import sys
import json
from pathlib import Path
from typing import Dict, Any

# Add current directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

try:
    from config_manager import ConfigManager, get_config_manager
except ImportError:
    print("Error: config_manager.py not found. Please ensure all files are present.")
    sys.exit(1)


class ConfigSetup:
    """Configuration setup utility for WallpaperChanger"""
    
    def __init__(self):
        self.config_manager = get_config_manager()
        self.script_dir = Path(__file__).parent
        
    def run_interactive_setup(self) -> None:
        """Run interactive configuration setup"""
        print("=" * 60)
        print("WallpaperChanger - Configuration Setup")
        print("=" * 60)
        print()
        
        # Check existing configuration
        self._check_existing_config()
        
        # Setup .env file
        self._setup_env_file()
        
        # Setup JSON config
        self._setup_json_config()
        
        # API key setup
        self._setup_api_keys()
        
        # Provider configuration
        self._setup_providers()
        
        # Final summary
        self._show_summary()
    
    def _check_existing_config(self) -> None:
        """Check for existing configuration files"""
        print("🔍 Checking existing configuration...")
        
        env_exists = self.config_manager.env_file.exists()
        json_exists = self.config_manager.json_file.exists()
        
        if env_exists:
            print(f"✅ .env file found: {self.config_manager.env_file}")
        else:
            print(f"❌ .env file not found: {self.config_manager.env_file}")
        
        if json_exists:
            print(f"✅ config.json found: {self.config_manager.json_file}")
        else:
            print(f"❌ config.json not found: {self.config_manager.json_file}")
        
        print()
    
    def _setup_env_file(self) -> None:
        """Setup .env file from template"""
        if self.config_manager.env_file.exists():
            response = input(".env file already exists. Overwrite? (y/N): ").strip().lower()
            if response != 'y':
                print("⏭️  Skipping .env file creation")
                print()
                return
        
        print("📝 Creating .env file from template...")
        
        if self.config_manager.create_env_file():
            print("✅ .env file created successfully")
        else:
            print("❌ Failed to create .env file")
        
        print()
    
    def _setup_json_config(self) -> None:
        """Setup JSON config from template"""
        if self.config_manager.json_file.exists():
            response = input("config.json already exists. Overwrite? (y/N): ").strip().lower()
            if response != 'y':
                print("⏭️  Skipping config.json creation")
                print()
                return
        
        print("📝 Creating config.json from template...")
        
        if self.config_manager.create_json_config():
            print("✅ config.json created successfully")
        else:
            print("❌ Failed to create config.json")
        
        print()
    
    def _setup_api_keys(self) -> None:
        """Interactive API key setup"""
        print("🔑 API Key Setup")
        print("-" * 30)
        
        api_providers = {
            'wallhaven': {
                'name': 'Wallhaven',
                'url': 'https://wallhaven.cc/settings/account',
                'required': True
            },
            'pexels': {
                'name': 'Pexels',
                'url': 'https://www.pexels.com/api/new/',
                'required': True
            },
            'unsplash': {
                'name': 'Unsplash',
                'url': 'https://unsplash.com/developers',
                'required': False
            },
            'pixabay': {
                'name': 'Pixabay',
                'url': 'https://pixabay.com/api/docs/',
                'required': False
            },
            'gemini': {
                'name': 'Google Gemini (AI Features)',
                'url': 'https://makersuite.google.com/app/apikey',
                'required': False
            },
            'openweather': {
                'name': 'OpenWeatherMap (Weather Integration)',
                'url': 'https://openweathermap.org/api',
                'required': False
            }
        }
        
        for provider, info in api_providers.items():
            current_key = self.config_manager.get_api_key(provider)
            status = "✅ Set" if current_key else "❌ Missing"
            
            print(f"\n{info['name']} API Key {status}")
            print(f"Get your key at: {info['url']}")
            
            if current_key:
                print(f"Current key: {current_key[:10]}...{current_key[-4:] if len(current_key) > 14 else current_key}")
                update = input("Update this key? (y/N): ").strip().lower()
                if update != 'y':
                    continue
            
            new_key = input("Enter API key (or press Enter to skip): ").strip()
            if new_key:
                # Save to both .env and JSON
                env_key = provider.upper() + '_API_KEY'
                os.environ[env_key] = new_key
                self.config_manager.update_json_value(f'api_keys.{provider}.key', new_key)
                print(f"✅ {info['name']} API key saved")
            elif info['required']:
                print(f"⚠️  Warning: {info['name']} API key is required for full functionality")
        
        print()
    
    def _setup_providers(self) -> None:
        """Setup wallpaper providers"""
        print("🖼️  Provider Configuration")
        print("-" * 30)
        
        # Get current settings
        default_provider = self.config_manager.get_default_provider()
        rotation_enabled = self.config_manager.is_rotation_enabled()
        rotation_sequence = self.config_manager.get_rotation_sequence()
        
        print(f"Current default provider: {default_provider}")
        print(f"Provider rotation: {'Enabled' if rotation_enabled else 'Disabled'}")
        if rotation_enabled:
            print(f"Rotation sequence: {', '.join(rotation_sequence)}")
        
        print()
        
        # Ask for changes
        new_default = input(f"Default provider [{default_provider}]: ").strip()
        if new_default:
            self.config_manager.update_json_value('providers.default', new_default)
            print(f"✅ Default provider set to {new_default}")
        
        rotation_choice = input(f"Enable provider rotation? [{'Y' if rotation_enabled else 'N'}]: ").strip().lower()
        if rotation_choice in ('y', 'yes', 'n', 'no'):
            new_rotation = rotation_choice in ('y', 'yes')
            self.config_manager.update_json_value('providers.rotation_enabled', new_rotation)
            print(f"✅ Provider rotation {'enabled' if new_rotation else 'disabled'}")
        
        print()
    
    def _show_summary(self) -> None:
        """Show configuration summary"""
        print("📊 Configuration Summary")
        print("=" * 40)
        
        summary = self.config_manager.get_config_summary()
        
        print(f"📁 .env file: {'✅' if summary['env_file_exists'] else '❌'}")
        print(f"📄 config.json: {'✅' if summary['json_file_exists'] else '❌'}")
        print(f"🎯 Default provider: {summary['default_provider']}")
        print(f"🔄 Provider rotation: {'✅' if summary['rotation_enabled'] else '❌'}")
        
        print("\n🔑 API Keys Status:")
        for provider, valid in summary['api_keys_validation'].items():
            status = "✅" if valid else "❌"
            print(f"  {provider.capitalize()}: {status}")
        
        print(f"\n🖼️  Enabled Providers: {', '.join(summary['enabled_providers'])}")
        
        print("\n🎉 Setup complete!")
        print("You can now start WallpaperChanger with:")
        print("  python gui_modern.py")
        print("  python main.py")
        print()
    
    def create_minimal_config(self) -> None:
        """Create minimal configuration for quick start"""
        print("🚀 Creating minimal configuration...")
        
        # Create .env file
        if not self.config_manager.env_file.exists():
            self.config_manager.create_env_file()
        
        # Create JSON config with minimal settings
        minimal_config = {
            "providers": {
                "default": "reddit",
                "rotation_enabled": False,
                "reddit": {
                    "enabled": True,
                    "subreddits": ["wallpapers", "wallpaper"],
                    "sort": "hot",
                    "limit": 25
                }
            },
            "application": {
                "auto_rotate": False,
                "change_interval_minutes": 60
            }
        }
        
        self.config_manager.save_json_config(minimal_config)
        print("✅ Minimal configuration created")
        print("🎯 Default provider: Reddit (no API key required)")


def main():
    """Main entry point"""
    setup = ConfigSetup()
    
    if len(sys.argv) > 1 and sys.argv[1] == '--minimal':
        setup.create_minimal_config()
    else:
        setup.run_interactive_setup()


if __name__ == "__main__":
    main()
