"""
Logging utilities
"""

import logging
import sys
from typing import Optional
from utils.config import Config  # Changed from 'from config import Config'

class LogManager:
    """Logger setup and management"""
    
    _instance = None  # Singleton instance
    _loggers = {}  # Dictionary of loggers
    
    def __new__(cls):
        """Create singleton instance"""
        if cls._instance is None:
            cls._instance = super(LogManager, cls).__new__(cls)
            cls._instance._setup_root_logger()
        return cls._instance
    
    def _setup_root_logger(self):
        """Set up the root logger"""
        config = Config()
        level = getattr(logging, config.get('logging', 'level', 'INFO'))
        log_format = config.get('logging', 'format', '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        log_file = config.get('logging', 'file', None)
        
        # Configure root logger
        root_logger = logging.getLogger()
        root_logger.setLevel(level)
        
        # Remove existing handlers
        for handler in root_logger.handlers[:]:
            root_logger.removeHandler(handler)
        
        # Create formatter
        formatter = logging.Formatter(log_format)
        
        # Create console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        root_logger.addHandler(console_handler)
        
        # Add file handler if specified
        if log_file:
            file_handler = logging.FileHandler(log_file)
            file_handler.setFormatter(formatter)
            root_logger.addHandler(file_handler)
    
    def get_logger(self, name: str) -> logging.Logger:
        """Get or create a logger with the given name"""
        if name not in self._loggers:
            logger = logging.getLogger(name)
            self._loggers[name] = logger
        return self._loggers[name]
    