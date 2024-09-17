import os
from dotenv import load_dotenv
load_dotenv()

from .llm_provider import LLMProvider
import google.generativeai as genai


genai.configure(api_key=os.environ["GEMINI_API_KEY"])

class GeminiClient(LLMProvider):
    def __init__(self, primer=None):
        self.provider = 'gemini'
        self.models = self.list_models()
        self.model = 'gemini-1.5-flash'
        self.client = genai.GenerativeModel(
            model_name=self.model,
            system_instruction=primer
        )
        
        self.messages = []
        self._chat = self.client.start_chat()
          

    def list_models(self):
        return ['gemini-1.5-flash']


    def chat(self, message):
        current_message = ""
        response_stream = self._chat.send_message(message, stream=True)
        for chunk in response_stream:
            delta = chunk.text
            current_message += delta
            yield delta

        self.messages.append({"role": "user", "parts": message})
        self.messages.append({"role": "model", "parts": current_message})
        return current_message



if __name__ == "__main__":
    client = GeminiClient(primer="Limit your response to 300 characters or less")
    for text in client.chat("I'm traveling to Madrid soon (mid-October) with my wife. We love food, history and shopping. We've been there before. Can you recommend a few destinations/activities off the beaten path? We're staying in the city center and will be there for 3 days. We're looking for authentic experiences, not tourist traps."):
        print(text, end="", flush=True)
    print()

    print(client.list_models())