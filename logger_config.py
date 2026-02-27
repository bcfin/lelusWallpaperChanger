"""
WallpaperChanger Logging Configuration
Provides centralized logging system with file and console output
"""

import logging
import logging.handlers
import os
import sys
from pathlib import Path
from datetime import datetime
from typing import Optional


class WallpaperChangerLogger:
    """Centralized logging system for WallpaperChanger"""
    
    def __init__(self, name: str = "WallpaperChanger", log_dir: Optional[str] = None):
        self.name = name
        self.log_dir = Path(log_dir) if log_dir else Path(__file__).parent
        self.log_file = self.log_dir / "debug.log"
        self.error_log_file = self.log_dir / "error.log"
        
        # Create log directory if it doesn't exist
        self.log_dir.mkdir(exist_ok=True)
        
        # Configure logging
        self._setup_logging()
    
    def _setup_logging(self) -> None:
        """Setup logging configuration"""
        # Create formatters
        detailed_formatter = logging.Formatter(
            fmt='%(asctime)s | %(levelname)-8s | %(name)-15s | %(funcName)-20s:%(lineno)-4d | %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        simple_formatter = logging.Formatter(
            fmt='%(asctime)s | %(levelname)-8s | %(message)s',
            datefmt='%H:%M:%S'
        )
        
        # Create handlers
        handlers = []
        
        # File handler for all logs
        file_handler = logging.handlers.RotatingFileHandler(
            filename=self.log_file,
            maxBytes=10*1024*1024,  # 10MB
            backupCount=5,
            encoding='utf-8'
        )
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(detailed_formatter)
        handlers.append(file_handler)
        
        # Separate error log file
        error_handler = logging.handlers.RotatingFileHandler(
            filename=self.error_log_file,
            maxBytes=5*1024*1024,  # 5MB
            backupCount=3,
            encoding='utf-8'
        )
        error_handler.setLevel(logging.ERROR)
        error_handler.setFormatter(detailed_formatter)
        handlers.append(error_handler)
        
        # Console handler (only when running from terminal)
        if sys.stdout.isatty() or os.getenv('DEBUG_CONSOLE', '').lower() == 'true':
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setLevel(logging.INFO)
            console_handler.setFormatter(simple_formatter)
            handlers.append(console_handler)
        
        # Configure root logger
        root_logger = logging.getLogger(self.name)
        root_logger.setLevel(logging.DEBUG)
        
        # Remove existing handlers to avoid duplicates
        for handler in root_logger.handlers[:]:
            root_logger.removeHandler(handler)
        
        # Add new handlers
        for handler in handlers:
            root_logger.addHandler(handler)
        
        # Store reference for easy access
        self.logger = root_logger
        
        # Log initialization
        self.logger.info("=" * 60)
        self.logger.info(f"WallpaperChanger Logging System Initialized")
        self.logger.info(f"Log file: {self.log_file}")
        self.logger.info(f"Error log file: {self.error_log_file}")
        self.logger.info(f"Python version: {sys.version}")
        self.logger.info(f"Working directory: {Path.cwd()}")
        self.logger.info("=" * 60)
    
    def get_logger(self, name: Optional[str] = None) -> logging.Logger:
        """Get a logger instance"""
        if name:
            return logging.getLogger(f"{self.name}.{name}")
        return self.logger
    
    def set_level(self, level: str) -> None:
        """Set logging level"""
        level_map = {
            'DEBUG': logging.DEBUG,
            'INFO': logging.INFO,
            'WARNING': logging.WARNING,
            'ERROR': logging.ERROR,
            'CRITICAL': logging.CRITICAL
        }
        
        log_level = level_map.get(level.upper(), logging.INFO)
        self.logger.setLevel(log_level)
        self.logger.info(f"Logging level set to {level.upper()}")
    
    def log_exception(self, exc_info, context: str = "") -> None:
        """Log exception with context"""
        if context:
            self.logger.error(f"Exception in {context}:", exc_info=exc_info)
        else:
            self.logger.error("Exception occurred:", exc_info=exc_info)
    
    def log_function_call(self, func_name: str, args: tuple = (), kwargs: dict = None) -> None:
        """Log function call for debugging"""
        kwargs = kwargs or {}
        args_str = ", ".join([str(arg) for arg in args])
        kwargs_str = ", ".join([f"{k}={v}" for k, v in kwargs.items()])
        
        all_args = []
        if args_str:
            all_args.append(args_str)
        if kwargs_str:
            all_args.append(kwargs_str)
        
        args_display = ", ".join(all_args)
        self.logger.debug(f"CALL {func_name}({args_display})")
    
    def log_api_request(self, provider: str, url: str, status_code: Optional[int] = None) -> None:
        """Log API request"""
        if status_code:
            self.logger.info(f"API Request [{provider}] {url} -> {status_code}")
        else:
            self.logger.info(f"API Request [{provider}] {url}")
    
    def log_wallpaper_change(self, source: str, path: str, trigger: str = "manual") -> None:
        """Log wallpaper change"""
        self.logger.info(f"WALLPAPER_CHANGED [{trigger}] {source}: {path}")
    
    def log_config_change(self, key: str, old_value: str, new_value: str) -> None:
        """Log configuration change"""
        self.logger.info(f"CONFIG_CHANGED {key}: '{old_value}' -> '{new_value}'")
    
    def create_crash_report(self, exc_info, context: str = "") -> str:
        """Create detailed crash report"""
        crash_report = []
        crash_report.append("=" * 60)
        crash_report.append("WALLPAPER CHANGER CRASH REPORT")
        crash_report.append("=" * 60)
        crash_report.append(f"Timestamp: {datetime.now().isoformat()}")
        crash_report.append(f"Context: {context}")
        crash_report.append(f"Python Version: {sys.version}")
        crash_report.append(f"Working Directory: {Path.cwd()}")
        crash_report.append("")
        
        if context:
            crash_report.append("CONTEXT:")
            crash_report.append(context)
            crash_report.append("")
        
        # Exception details
        import traceback
        crash_report.append("EXCEPTION:")
        crash_report.append("".join(traceback.format_exception(*exc_info)))
        crash_report.append("")
        
        # System info
        try:
            import platform
            crash_report.append("SYSTEM INFO:")
            crash_report.append(f"OS: {platform.system()} {platform.release()}")
            crash_report.append(f"Architecture: {platform.machine()}")
            crash_report.append(f"Processor: {platform.processor()}")
        except:
            crash_report.append("System info unavailable")
        
        crash_report.append("")
        crash_report.append("=" * 60)
        
        report_content = "\n".join(crash_report)
        
        # Save crash report
        crash_file = self.log_dir / f"crash_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        try:
            with open(crash_file, 'w', encoding='utf-8') as f:
                f.write(report_content)
            self.logger.error(f"Crash report saved to: {crash_file}")
        except Exception as e:
            self.logger.error(f"Failed to save crash report: {e}")
        
        return report_content


# Global logger instance
_logger_instance: Optional[WallpaperChangerLogger] = None


def get_logger(name: Optional[str] = None) -> logging.Logger:
    """Get the global logger instance"""
    global _logger_instance
    if _logger_instance is None:
        _logger_instance = WallpaperChangerLogger()
    return _logger_instance.get_logger(name)


def setup_logging(log_level: str = "INFO", log_dir: Optional[str] = None) -> None:
    """Setup the global logging system"""
    global _logger_instance
    _logger_instance = WallpaperChangerLogger(log_dir=log_dir)
    _logger_instance.set_level(log_level)


def log_exception(exc_info, context: str = "") -> None:
    """Log exception using global logger"""
    logger = get_logger()
    if hasattr(_logger_instance, 'log_exception'):
        _logger_instance.log_exception(exc_info, context)
    else:
        logger.error(f"Exception in {context}:", exc_info=exc_info)


def log_api_request(provider: str, url: str, status_code: Optional[int] = None) -> None:
    """Log API request using global logger"""
    logger = get_logger()
    if hasattr(_logger_instance, 'log_api_request'):
        _logger_instance.log_api_request(provider, url, status_code)
    else:
        if status_code:
            logger.info(f"API Request [{provider}] {url} -> {status_code}")
        else:
            logger.info(f"API Request [{provider}] {url}")


def log_wallpaper_change(source: str, path: str, trigger: str = "manual") -> None:
    """Log wallpaper change using global logger"""
    logger = get_logger()
    if hasattr(_logger_instance, 'log_wallpaper_change'):
        _logger_instance.log_wallpaper_change(source, path, trigger)
    else:
        logger.info(f"WALLPAPER_CHANGED [{trigger}] {source}: {path}")


# Decorators for automatic logging
def log_function_calls(logger_name: Optional[str] = None):
    """Decorator to log function calls"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            logger = get_logger(logger_name)
            logger.debug(f"ENTER {func.__name__}({args}, {kwargs})")
            try:
                result = func(*args, **kwargs)
                logger.debug(f"EXIT {func.__name__} -> {result}")
                return result
            except Exception as e:
                logger.error(f"ERROR in {func.__name__}: {e}")
                raise
        return wrapper
    return decorator


def log_exceptions(context: str = ""):
    """Decorator to log exceptions"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                log_exception(sys.exc_info(), f"{context}.{func.__name__}")
                raise
        return wrapper
    return decorator
