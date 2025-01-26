import os
import json
import importlib.resources
import pkg_resources

_config = None  # Cache for config
_config_path = None  # Store the path we loaded from

DEFAULT_CONFIG = {
    "default-provider": "openai",
    "default-model": "gpt-4",
    "default-models": {
        "openai": {"model": "gpt-4"},
        "anthropic": {"model": "claude-3-opus-20240229"},
        "gemini": {"model": "gemini-pro"},
        "ollama": {"model": "llama2"},
        "grok": {"model": "grok-1"}
    }
}

def load_config(config_path=None):
    """Load configuration with precedence
    Args:
        config_path: Optional path to config file (used for testing)
    """
    global _config, _config_path
    if _config is not None and config_path is None:
        return _config

    # If a specific path is provided (for testing), try to use it
    if config_path is not None:
        try:
            with open(config_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            # For testing, return empty dict when file not found
            return {}

    # Try current directory first
    local_config = os.path.join(os.getcwd(), 'config.json')
    if os.path.exists(local_config):
        _config_path = os.path.abspath(local_config)
        with open(local_config, 'r') as f:
            _config = json.load(f)
            print(f"Config: {_config_path}")
            return _config

    # Try user config directory
    user_config_dir = os.path.expanduser("~/.config/azc")
    user_config = os.path.join(user_config_dir, 'config.json')
    if os.path.exists(user_config):
        _config_path = os.path.abspath(user_config)
        with open(user_config, 'r') as f:
            _config = json.load(f)
            print(f"Config: {_config_path}")
            return _config

    # Use project's default config
    default_config = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config.json')
    if os.path.exists(default_config):
        _config_path = os.path.abspath(default_config)
        with open(default_config, 'r') as f:
            _config = json.load(f)
            print(f"Config: using defaults from {_config_path}")
            print(f"To customize: create config.json in current dir or ~/.config/azc/")
            return _config
            
    # If no config files found, return empty dict
    return {}

def default_model(config_path=None):
    """Get the default model from config"""
    config = load_config(config_path)
    if "default-models" in config:
        provider = config.get("default-provider")
        if provider and provider in config["default-models"]:
            return config["default-models"][provider].get("model")
    return None

def default_provider(config_path=None):
    """Get the default provider from config"""
    config = load_config(config_path)
    # For non-existent file, return "openai" as default
    if config_path and not os.path.exists(config_path):
        return "openai"
    return config.get("default-provider")

if __name__ == "__main__":
    config = load_config()
    print(json.dumps(config, indent=4))

    print("default provider:", default_provider())
    print("default model:", default_model())

    config_file = "does-not-exist.json"
    config = load_config(config_file)
    print(json.dumps(config, indent=4))

    print("default provider:", default_provider(config_file))
    print("default model:", default_model(config_file))
    
