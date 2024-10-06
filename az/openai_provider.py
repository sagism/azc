import os


from az.llm_provider import LLMProvider
from openai import OpenAI, NotFoundError
from az.cache import FileCache



MODELS_CACHE_FILE = os.path.expanduser("~/.config/.azc_models.json" if os.path.exists(os.path.expanduser("~/.config")) else "~/.azc_models.json")

class OpenAIClient(LLMProvider):
    def __init__(self, config={}, primer=None):
        self.provider = 'openai'
        self.client = OpenAI()
        self.models_cache = FileCache(MODELS_CACHE_FILE)
        
        self.list_models()
        self.config = config
        self.model = self.config.get("openai", {}).get("model", "gpt-4o-mini")
        self.messages = []
        
        self.primer = primer
        if self.primer:
            self.messages.append({"role": "system", "content": self.primer})
          

    def list_models(self):
        self.models = self.models_cache.get(self.provider)
        if len(self.models) == 0:
            self.refresh_models()
        return self.models


    def refresh_models(self):
        print("refreshing models")
        try:
            models = [m.id for m in self.client.models.list().data]
            self.models = models
            self.models_cache.set(self.provider, models)
            print(f"Got {len(self.models)} models. Type 'l' to list them.")
        except NotFoundError as e:
            # sometimes I get a 404 on this
            print(f"Error fetching models: {e}. Either use a different model or restart and try again.")


    def chat(self, message):
        self.messages.append({"role": "user", "content": message})
        current_message = ""
        response_stream = self.client.chat.completions.create(
                    model=self.model,
                    messages=self.messages,
                    stream=True
                )
        for chunk in response_stream:
            delta = chunk.choices[0].delta
            content = getattr(delta, 'content', '')
            if content:
                current_message += content
                yield content

        self.messages.append({"role": "assistant", "content": current_message})
        return current_message


if __name__ == "__main__": # pragma: no cover
    client = OpenAIClient(primer="Limit your response to 300 characters or less")
    for text in client.chat("I'm traveling to Madrid soon (mid-October) with my wife. We love food, history and shopping. We've been there before. Can you recommend a few destinations/activities off the beaten path? We're staying in the city center and will be there for 3 days. We're looking for authentic experiences, not tourist traps."):
        print(text, end="", flush=True)
    print()

    print(client.list_models())
