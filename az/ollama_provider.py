import json
import os

import requests
import httpx

from az.llm_provider import LLMProvider


class OllamaClient(LLMProvider):
    def __init__(self, config={}):
        LLMProvider.__init__(self)
        self.provider = 'ollama'
        self.name = 'ollama'
        base_url = os.getenv("OLLAMA_URL", "http://localhost:11434")
        base_url = base_url.rstrip('/')
        self.client = httpx.Client(
            base_url=base_url,
            timeout=40.0  # Set timeout to 40 seconds
        )
        self.config = config
        self.models = self.list_models()
        # Get model from config or use first available model as default
        self.model = self.config.get("ollama", {}).get("model") or (self.models[0] if self.models else "llama2")
        self.messages = []
        self.primer = config.get("primer")
        if self.primer:
            self.messages.append({"role": "system", "content": self.primer})

    def list_models(self):
        """List all models available from Ollama's /api/tags endpoint"""
        try:
            response = self.client.get("/api/tags")
            response.raise_for_status()
            
            if response.status_code == 200:
                models_data = response.json()["models"]
                return [model["name"] for model in models_data]
            else:
                print(f"Warning: Could not list models, using empty list")
                return []
                
        except Exception as e:
            print(f"Warning: Could not list models: {e}")
            return []

    @property
    def model(self):
        return self._model

    @model.setter
    def model(self, value):
        # For Ollama, just accept any model name as it might be pulled on demand
        self._model = value

    def chat(self, message):
        if self.primer and len(self.messages) == 0:
            self.messages.append({"role": "user", "content": self.primer + "\n\n" + message})
        else:
            self.messages.append({"role": "user", "content": message})

        try:
            with self.client.stream('POST', "/api/chat", json={
                "model": self.model,
                "messages": self.messages,
                "stream": True
            }) as response:
                response.raise_for_status()
                collected_message = []

                for chunk in response.iter_bytes():
                    if not chunk:
                        continue
                        
                    try:
                        data = json.loads(chunk)
                        if data.get('done', False):
                            continue
                        if 'message' in data and 'content' in data['message']:
                            content = data['message']['content']
                            # Skip the thinking tokens if present.
                            if content == '<think>':
                                content = 'thinking...\n'
                            elif content == '</think>':
                                content = '... done thinking.\n'
                            collected_message.append(content)
                            yield content
                    except json.JSONDecodeError:
                        continue

                # Add the complete message to history
                full_response = ''.join(collected_message)
                self.messages.append({"role": "assistant", "content": full_response})

        except httpx.HTTPError as e:
            error_message = f"Ollama API error: {str(e)}"
            print(f"\n[red]{error_message}[/red]")
            return
        except Exception as e:
            error_message = f"Unexpected error: {str(e)}"
            print(f"\n[red]{error_message}[/red]")
            return


def test_ollama(model="llama2", prompt="Tell me a short story about a robot"):
    """Test function for Ollama provider"""
    print(f"\nTesting Ollama with model: {model}")
    print(f"Prompt: {prompt}")
    print("\nResponse:")
    
    try:
        client = OllamaClient({"ollama": {"model": model}})
        print("Models:")
        print(client.list_models())
        for chunk in client.chat(prompt):
            print(chunk, end='', flush=True)
        print("\n\nTest completed.")
        
    except Exception as e:
        print(f"\nError during test: {str(e)}")

if __name__ == "__main__":
    import sys
    
    # Get model and prompt from command line arguments, or use defaults
    model = sys.argv[1] if len(sys.argv) > 1 else "llama2"
    prompt = sys.argv[2] if len(sys.argv) > 2 else "Tell me a short story about a robot"
    
    test_ollama(model, prompt)
