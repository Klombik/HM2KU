import json
import os
from datetime import datetime
from src.exceptions import ConfigError

def load_config(config_path: str) -> dict:
    """Загружает конфигурацию из JSON файла и проверяет ее."""
    if not os.path.exists(config_path):
        raise ConfigError(f"Config file not found: {config_path}")
    
    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
    except json.JSONDecodeError:
        raise ConfigError(f"Invalid JSON format in config file: {config_path}")

    # Проверки конфигурации
    if not isinstance(config, dict):
        raise ConfigError("Config must be a JSON object")
    if not all(key in config for key in ["graphviz_path", "repo_path", "output_path", "since_date"]):
         raise ConfigError("Config must contain 'graphviz_path', 'repo_path', 'output_path' and 'since_date' keys")
    if not os.path.exists(config["repo_path"]):
        raise ConfigError(f"Repository path does not exist: {config['repo_path']}")
    if not os.path.exists(config["graphviz_path"]):
        raise ConfigError(f"Graphviz executable does not exist: {config['graphviz_path']}")

    try:
         datetime.fromisoformat(config["since_date"])
    except ValueError:
         raise ConfigError(f"Invalid date format in config: {config['since_date']}")


    return config