"""
Configuration Manager for WallpaperChanger
Handles both .env and JSON configuration files with validation and type conversion
"""

import json
import os
import logging
from pathlib import Path
from typing import Dict, Any, Optional, Union, List
from dataclasses import dataclass
from dotenv import load_dotenv


@dataclass
class APIKeyConfig:
    """Configuration for API keys"""
    key: str
    description: str
    required: bool = False
    provider: Optional[str] = None
    service: Optional[str] = None


class ConfigManager:
    """Manages application configuration from .env and JSON files"""
    
    def __init__(self, config_dir: Optional[str] = None):
        self.config_dir = Path(config_dir) if config_dir else Path(__file__).parent
        self.env_file = self.config_dir / '.env'
        self.json_file = self.config_dir / 'config.json'
        self.json_template = self.config_dir / 'config.template.json'
        self.env_example = self.config_dir / '.env.example'
        
        self.logger = logging.getLogger(__name__)
        self._config_cache: Dict[str, Any] = {}
        
        # Load configurations
        self._load_env()
        self._load_json()
    
    def _load_env(self) -> None:
        """Load environment variables from .env file"""
        if self.env_file.exists():
            load_dotenv(dotenv_path=self.env_file)
            self.logger.info(f"Loaded environment variables from {self.env_file}")
        else:
            self.logger.warning(f".env file not found at {self.env_file}")
    
    def _load_json(self) -> None:
        """Load configuration from JSON file"""
        if self.json_file.exists():
            try:
                with open(self.json_file, 'r', encoding='utf-8') as f:
                    self._config_cache = json.load(f)
                self.logger.info(f"Loaded JSON configuration from {self.json_file}")
            except json.JSONDecodeError as e:
                self.logger.error(f"Invalid JSON in {self.json_file}: {e}")
                self._config_cache = {}
        else:
            self.logger.info(f"JSON config file not found, using defaults")
            self._config_cache = {}
    
    def get_env(self, key: str, default: Any = None, cast_type: type = str) -> Any:
        """Get environment variable with type casting"""
        value = os.getenv(key, default)
        
        if value is None or value == default:
            return default
        
        try:
            if cast_type == bool:
                return value.lower() in ('true', '1', 'yes', 'on')
            elif cast_type == int:
                return int(value)
            elif cast_type == float:
                return float(value)
            elif cast_type == list:
                return [item.strip() for item in value.split(',') if item.strip()]
            else:
                return cast_type(value)
        except (ValueError, TypeError) as e:
            self.logger.warning(f"Failed to cast {key}={value} to {cast_type}: {e}")
            return default
    
    def get_json(self, key_path: str, default: Any = None) -> Any:
        """Get value from JSON config using dot notation (e.g., 'providers.wallhaven.enabled')"""
        if not self._config_cache:
            return default
        
        keys = key_path.split('.')
        value = self._config_cache
        
        try:
            for key in keys:
                value = value[key]
            return value
        except (KeyError, TypeError):
            return default
    
    def get_api_key(self, provider: str) -> Optional[str]:
        """Get API key for a specific provider"""
        # Try JSON config first
        json_key = self.get_json(f'api_keys.{provider}.key')
        if json_key and json_key != f'your_{provider}_api_key_here':
            return json_key
        
        # Fall back to environment variable
        env_key = provider.upper() + '_API_KEY'
        env_value = self.get_env(env_key)
        if env_value and env_value != f'your_{provider}_api_key_here':
            return env_value
        
        return None
    
    def get_provider_config(self, provider: str) -> Dict[str, Any]:
        """Get complete configuration for a provider"""
        # Get provider-specific config from JSON
        provider_config = self.get_json(f'providers.{provider}', {})
        
        # Add API key if available
        api_key = self.get_api_key(provider)
        if api_key:
            provider_config['api_key'] = api_key
        
        return provider_config
    
    def is_provider_enabled(self, provider: str) -> bool:
        """Check if a provider is enabled"""
        # Check JSON config
        enabled = self.get_json(f'providers.{provider}.enabled')
        if enabled is not None:
            return enabled
        
        # Fall back to environment variables or defaults
        if provider == 'reddit':
            return True  # Reddit is always enabled (no API key required)
        
        # Check if API key is available for other providers
        return self.get_api_key(provider) is not None
    
    def get_default_provider(self) -> str:
        """Get the default wallpaper provider"""
        # Try JSON config first
        default = self.get_json('providers.default')
        if default:
            return default
        
        # Fall back to environment variable
        return self.get_env('DEFAULT_PROVIDER', 'reddit')
    
    def get_rotation_sequence(self) -> List[str]:
        """Get the provider rotation sequence"""
        # Try JSON config first
        sequence = self.get_json('providers.rotation_sequence')
        if sequence:
            return sequence
        
        # Fall back to environment variable
        return self.get_env('PROVIDER_SEQUENCE', ['wallhaven', 'pexels', 'reddit'], list)
    
    def is_rotation_enabled(self) -> bool:
        """Check if provider rotation is enabled"""
        # Try JSON config first
        enabled = self.get_json('providers.rotation_enabled')
        if enabled is not None:
            return enabled
        
        # Fall back to environment variable
        return self.get_env('ENABLE_PROVIDER_ROTATION', True, bool)
    
    def save_json_config(self, config: Dict[str, Any]) -> bool:
        """Save configuration to JSON file"""
        try:
            with open(self.json_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
            
            # Reload the configuration
            self._load_json()
            self.logger.info(f"Saved JSON configuration to {self.json_file}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to save JSON config: {e}")
            return False
    
    def update_json_value(self, key_path: str, value: Any) -> bool:
        """Update a specific value in JSON config using dot notation"""
        if not self._config_cache:
            # Load template if no config exists
            if self.json_template.exists():
                with open(self.json_template, 'r', encoding='utf-8') as f:
                    self._config_cache = json.load(f)
            else:
                self._config_cache = {}
        
        keys = key_path.split('.')
        config = self._config_cache
        
        # Navigate to the parent of the target key
        for key in keys[:-1]:
            if key not in config:
                config[key] = {}
            config = config[key]
        
        # Set the value
        config[keys[-1]] = value
        
        # Save the updated configuration
        return self.save_json_config(self._config_cache)
    
    def create_env_file(self) -> bool:
        """Create .env file from .env.example"""
        if not self.env_example.exists():
            self.logger.error(f".env.example not found at {self.env_example}")
            return False
        
        try:
            with open(self.env_example, 'r', encoding='utf-8') as src:
                content = src.read()
            
            with open(self.env_file, 'w', encoding='utf-8') as dst:
                dst.write(content)
            
            self.logger.info(f"Created .env file from template")
            return True
        except Exception as e:
            self.logger.error(f"Failed to create .env file: {e}")
            return False
    
    def create_json_config(self) -> bool:
        """Create config.json file from template"""
        if not self.json_template.exists():
            self.logger.error(f"config.template.json not found at {self.json_template}")
            return False
        
        try:
            with open(self.json_template, 'r', encoding='utf-8') as src:
                template = json.load(src)
            
            with open(self.json_file, 'w', encoding='utf-8') as dst:
                json.dump(template, dst, indent=2, ensure_ascii=False)
            
            self.logger.info(f"Created config.json from template")
            return True
        except Exception as e:
            self.logger.error(f"Failed to create config.json: {e}")
            return False
    
    def validate_api_keys(self) -> Dict[str, bool]:
        """Validate all required API keys"""
        providers = ['wallhaven', 'pexels', 'unsplash', 'pixabay']
        validation = {}
        
        for provider in providers:
            api_key = self.get_api_key(provider)
            is_required = self.get_json(f'api_keys.{provider}.required', False)
            
            if is_required and not api_key:
                validation[provider] = False
            elif api_key and api_key != f'your_{provider}_api_key_here':
                validation[provider] = True
            else:
                validation[provider] = not is_required
        
        return validation
    
    def get_all_api_keys_info(self) -> Dict[str, APIKeyConfig]:
        """Get information about all API keys"""
        info = {}
        
        # Get from JSON config
        if self._config_cache and 'api_keys' in self._config_cache:
            for provider, data in self._config_cache['api_keys'].items():
                info[provider] = APIKeyConfig(
                    key=data.get('key', ''),
                    description=data.get('description', ''),
                    required=data.get('required', False),
                    provider=data.get('provider'),
                    service=data.get('service')
                )
        
        # Add defaults for missing providers
        defaults = {
            'wallhaven': APIKeyConfig(
                key=self.get_env('WALLHAVEN_API_KEY', ''),
                description='Get your API key from https://wallhaven.cc/settings/account',
                required=True,
                provider='wallhaven'
            ),
            'pexels': APIKeyConfig(
                key=self.get_env('PEXELS_API_KEY', ''),
                description='Get your API key from https://www.pexels.com/api/new/',
                required=True,
                provider='pexels'
            )
        }
        
        for provider, config in defaults.items():
            if provider not in info:
                info[provider] = config
        
        return info
    
    def get_config_summary(self) -> Dict[str, Any]:
        """Get a summary of current configuration"""
        return {
            'env_file_exists': self.env_file.exists(),
            'json_file_exists': self.json_file.exists(),
            'default_provider': self.get_default_provider(),
            'rotation_enabled': self.is_rotation_enabled(),
            'rotation_sequence': self.get_rotation_sequence(),
            'api_keys_validation': self.validate_api_keys(),
            'enabled_providers': [p for p in ['wallhaven', 'pexels', 'reddit', 'unsplash', 'pixabay'] 
                                if self.is_provider_enabled(p)]
        }


# Global instance for easy access
_config_manager_instance: Optional[ConfigManager] = None


def get_config_manager() -> ConfigManager:
    """Get the global configuration manager instance"""
    global _config_manager_instance
    if _config_manager_instance is None:
        _config_manager_instance = ConfigManager()
    return _config_manager_instance


def reset_config_manager() -> None:
    """Reset the global configuration manager instance"""
    global _config_manager_instance
    _config_manager_instance = None
