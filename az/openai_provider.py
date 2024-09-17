from dotenv import load_dotenv
load_dotenv()

from .llm_provider import LLMProvider
from openai import OpenAI


class OpenAIClient(LLMProvider):
    def __init__(self, primer=None):
        self.provider = 'openai'
        self.client = OpenAI()
        self.models = self.list_models()
        self.model = 'gpt-4o-m'
        self.messages = []
        self.primer = primer
        if self.primer:
            self.messages.append({"role": "system", "content": self.primer})
          

    def list_models(self):
        return [m.id for m in self.client.models.list().data]
    



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



if __name__ == "__main__":
    client = OpenAIClient(primer="Limit your response to 300 characters or less")
    for text in client.chat("I'm traveling to Madrid soon (mid-October) with my wife. We love food, history and shopping. We've been there before. Can you recommend a few destinations/activities off the beaten path? We're staying in the city center and will be there for 3 days. We're looking for authentic experiences, not tourist traps."):
        print(text, end="", flush=True)
    print()

    print(client.list_models())