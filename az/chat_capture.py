import json
from datetime import datetime

class ChatCapture:
    def __init__(self):
        self.is_capturing = False
        self.capture_file = None

    def start(self):
        """Start capturing chat"""
        timestamp = datetime.now().strftime("%Y_%m_%d__%H_%M_%S")
        self.capture_file = f"capture_{timestamp}.json"
        self.is_capturing = True
        # Initialize the file with an empty messages array
        with open(self.capture_file, 'w', encoding='utf-8') as f:
            json.dump({"messages": []}, f, indent=2, ensure_ascii=False)

    def stop(self):
        """Stop capturing"""
        self.is_capturing = False
        self.capture_file = None

    def add_message(self, role: str, text: str, provider: str, model: str, tokens: int, is_markdown: bool = False):
        """Add a message directly to the capture file"""
        if not self.is_capturing:
            return
            
        message = {
            "role": str(role),
            "text": str(text),
            "provider": str(provider),
            "model": str(model),
            "timestamp": datetime.now().isoformat(),
            "tokens": int(tokens)
        }
        
        if is_markdown:
            message["format"] = "markdown"
            
        # Read current content
        with open(self.capture_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        # Append new message
        data["messages"].append(message)
        
        # Write back to file
        with open(self.capture_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False) 