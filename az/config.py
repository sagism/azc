import os
import json

def load_config(filename="config.json"):

    if not os.path.exists(filename):
        return {}
    with open(filename, "r") as f:
        return json.load(f)
    

if __name__ == "__main__":
    config = load_config()
    print(json.dumps(config, indent=4))
    
