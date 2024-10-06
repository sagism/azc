import os

from az.llm_provider import LLMProvider
import google.generativeai as genai


genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

class GeminiClient(LLMProvider):
    def __init__(self, config={}, primer=None):
        self.primer = primer
        self.provider = 'gemini'
        self.config = config

        self.models = self.list_models()
        self.model = self.config.get(self.provider, {}).get("model", "gemini-1.5-flash")
        
        self._n_user_messages = 0
        self.client = genai.GenerativeModel(
            model_name=self.model,
            system_instruction=self.primer
        )        
        self._chat = self.client.start_chat()
          

    def list_models(self):
        # I don't see a way to list models in the API
        return ['gemini-1.5-flash', 'gemini-1.5-pro']

    def n_user_messages(self):
        return self._n_user_messages

    def chat(self, message):
        current_message = ""
        response_stream = self._chat.send_message(message, stream=True)
        for chunk in response_stream:
            delta = chunk.text
            current_message += delta
            yield delta

        self._n_user_messages += 1
        return current_message

    def new_chat(self, primer=None):
        if primer:
            self.primer = primer
        self._chat = self.client.start_chat()
        self._n_user_messages = 0


if __name__ == "__main__": # pragma: no cover
    client = GeminiClient(primer="Limit your response to 300 characters or less")
    for text in client.chat("I'm traveling to Madrid soon (mid-October) with my wife. We love food, history and shopping. We've been there before. Can you recommend a few destinations/activities off the beaten path? We're staying in the city center and will be there for 3 days. We're looking for authentic experiences, not tourist traps."):
        print(text, end="", flush=True)
    print()

    print(client.list_models())
