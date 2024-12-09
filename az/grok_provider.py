from az.openai_provider import OpenAIClient
from az.llm_provider import LLMProvider
import os
from openai import OpenAI

class GrokClient(OpenAIClient):
    def __init__(self, config={}, primer=None):
        LLMProvider.__init__(self, primer)  # Call this first
        self.provider = 'grok'
        self.name = 'grok'
        self.client = OpenAI(
            api_key=os.getenv("XAI_API_KEY"),
            base_url="https://api.x.ai/v1"
        )
        self.config = config
        self.models = self.list_models()
        self.model = self.config.get("grok", {}).get("model", "grok-beta")
        
    def list_models(self):
        """Grok currently only has one model"""
        return ["grok-beta"]

if __name__ == "__main__": # pragma: no cover
    client = GrokClient(primer="You are Grok, inspired by Hitchhiker's Guide")
    for text in client.chat("What is the meaning of life?"):
        print(text, end="", flush=True)
    print() 