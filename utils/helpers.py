
import yaml
import json
import os
from pathlib import Path
from typing import Dict, Any, Optional

def load_yaml_config(file_path: str) -> Dict[str, Any]:
    """Load YAML configuration file"""
    try:
        with open(file_path, 'r') as file:
            return yaml.safe_load(file) or {}
    except FileNotFoundError:
        return {}
    except yaml.YAMLError as e:
        raise ValueError(f"Invalid YAML in {file_path}: {e}")

def load_json_config(file_path: str) -> Dict[str, Any]:
    """Load JSON configuration file"""
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON in {file_path}: {e}")

def load_config() -> Dict[str, Any]:
    """Load main configuration"""
    config_file = "config/config.yaml"
    if os.path.exists(config_file):
        return load_yaml_config(config_file)
    return {}

def ensure_directory(path: str):
    """Ensure directory exists"""
    Path(path).mkdir(parents=True, exist_ok=True)

def get_env_var(key: str, default: Optional[str] = None) -> Optional[str]:
    """Get environment variable with optional default"""
    return os.getenv(key, default)

def parse_bool(value: str) -> bool:
    """Parse string to boolean"""
    return value.lower() in ('true', '1', 'yes', 'on')

def safe_dict_get(data: dict, key: str, default=None):
    """Safely get value from nested dictionary"""
    keys = key.split('.')
    current = data
    
    for k in keys:
        if isinstance(current, dict) and k in current:
            current = current[k]
        else:
            return default
    
    return current

class ConfigValidator:
    """Validate configuration dictionaries"""
    
    @staticmethod
    def validate_agent_config(config: Dict[str, Any]) -> bool:
        """Validate agent configuration"""
        required_fields = ['name', 'enabled']
        return all(field in config for field in required_fields)
    
    @staticmethod
    def validate_framework_config(config: Dict[str, Any]) -> bool:
        """Validate framework configuration"""
        required_fields = ['framework', 'agents']
        return all(field in config for field in required_fields)