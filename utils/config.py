"""
Configuration management utilities
"""

import json
import os
from typing import Dict, Any, Optional

class Config:
    """Configuration management class"""
    
    _instance = None  # Singleton instance
    
    def __new__(cls):
        """Create singleton instance"""
        if cls._instance is None:
            cls._instance = super(Config, cls).__new__(cls)
            cls._instance._config = {}
            cls._instance._load_default_config()
        return cls._instance
    
    def _load_default_config(self):
        """Load default configuration"""
        self._config = {
            'logging': {
                'level': 'INFO',
                'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                'file': None
            },
            'calculation': {
                'parallel_processing': True,
                'max_workers': 4,
                'precision': 1e-8,
                'max_iterations': 100
            },
            'io': {
                'default_format': 'csv',
                'date_format': '%m/%d/%Y'
            }
        }
    
    def load_from_file(self, file_path: str) -> None:
        """Load configuration from file"""
        with open(file_path, 'r') as f:
            config = json.load(f)
            self._update_config(config)
    
    def load_from_env(self) -> None:
        """Load configuration from environment variables"""
        # Example: BOND_LIB_CALCULATION_PARALLEL_PROCESSING -> self._config['calculation']['parallel_processing']
        for key in os.environ:
            if key.startswith('BOND_LIB_'):
                parts = key[9:].lower().split('_')
                if len(parts) >= 2:
                    section = parts[0]
                    option = '_'.join(parts[1:])
                    if section in self._config and option in self._config[section]:
                        self._config[section][option] = self._parse_value(os.environ[key])
    
    def _parse_value(self, value: str) -> Any:
        """Parse string value to appropriate type"""
        if value.lower() in ('true', 'yes', '1'):
            return True
        if value.lower() in ('false', 'no', '0'):
            return False
        try:
            return int(value)
        except ValueError:
            try:
                return float(value)
            except ValueError:
                return value
    
    def _update_config(self, config: Dict[str, Any]) -> None:
        """Update configuration with new values"""
        for section, options in config.items():
            if section not in self._config:
                self._config[section] = {}
            if isinstance(options, dict):
                for option, value in options.items():
                    self._config[section][option] = value
    
    def get(self, section: str, option: str, default: Any = None) -> Any:
        """Get configuration value"""
        if section in self._config and option in self._config[section]:
            return self._config[section][option]
        return default
    
    def set(self, section: str, option: str, value: Any) -> None:
        """Set configuration value"""
        if section not in self._config:
            self._config[section] = {}
        self._config[section][option] = value
    
    def save_to_file(self, file_path: str) -> None:
        """Save configuration to file"""
        with open(file_path, 'w') as f:
            json.dump(self._config, f, indent=4)
            