import os
import json


def load_config(filename="config.json"):
    if not os.path.exists(filename):
        return {}
    with open(filename, "r") as f:
        return json.load(f)
    

def default_provider(filename="config.json"):
    config = load_config(filename)
    return config.get("default-provider", "openai")


def default_model(filename="config.json", provider=None):
    config = load_config(filename)
    if provider is None:
        provider = default_provider(filename)
    return config.get('default-models', {}).get(provider, {}).get("model")
    

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
    
