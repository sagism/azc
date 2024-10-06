import json
import os

import requests

from az.llm_provider import LLMProvider


class OllamaClient(LLMProvider):
    def __init__(self, primer=None):
        self.provider = "ollama"
        self.base_url = os.environ.get("OLLAMA_URL")
        self.models = self.list_models()  # List available models on initialization
        self.model = (
            self.models[0] if self.models else None
        )  # Set the first model as default
        self.messages = []
        self.primer = primer
        if self.primer:
            self.messages.append({"role": "system", "content": self.primer})

    def list_models(self):
        """List all models available from Ollama's /api/tags endpoint"""
        url = f"{self.base_url}/api/tags"
        response = requests.get(url)

        if response.status_code == 200:
            models_data = response.json()["models"]  # Extract the list of models
            return [
                model["name"] for model in models_data
            ]  # Return the 'name' of each model
        else:
            raise Exception(
                f"Failed to list models: {response.status_code} {response.text}"
            )

    def chat(self, message):
        """Chat with the model using Ollama's API"""
        self.messages.append({"role": "user", "content": message})
        current_message = ""

        # Update the URL to the correct chat endpoint
        url = f"{self.base_url}/api/chat"
        payload = {
            "model": self.model,  # The model to use for chat
            "messages": self.messages,  # The chat history including the primer
        }

        # Sending the chat request and streaming the response
        response_stream = requests.post(url, json=payload, stream=True)

        # Loop through the response lines (streamed chunks)
        for chunk in response_stream.iter_lines():
            if chunk:
                # Each chunk is a valid JSON object
                response_json = json.loads(chunk.decode("utf-8"))

                # Check if it's the final chunk with 'done' flag
                if response_json.get("done", False):
                    print("Final response:", response_json)  # For debugging purposes
                    break

                # Get the content of the message if available
                content = response_json.get("message", {}).get("content", "")
                current_message += content  # Append the content to the full message

                yield content  # Yield the content incrementally if needed

        # Add the final assistant message to the conversation history
        self.messages.append({"role": "assistant", "content": current_message})

        return current_message  # Return the final assembled message


if __name__ == "__main__": # pragma: no cover
    client = OllamaClient(primer="Limit your response to 300 characters or less")
    for text in client.chat(
        "I'm traveling to Madrid soon (mid-October) with my wife. We love food, history, and shopping. We've been there before. Can you recommend a few destinations/activities off the beaten path? We're staying in the city center and will be there for 3 days. We're looking for authentic experiences, not tourist traps."
    ):
        print(text, end="", flush=True)
    print()
