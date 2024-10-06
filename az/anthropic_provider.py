from az.llm_provider import LLMProvider
import anthropic



class AnthropicClient(LLMProvider):
    def __init__(self, config={}, primer=None):
        self.provider = 'anthropic'
        self.client = anthropic.Anthropic()
        self.models = self.list_models()
        self.config = config
        self.model = self.config.get("anthropic", {}).get("model", "claude-3-5-sonnet")
        self.messages = []
        self.primer = primer
          

    def list_models(self):
        """ No way to list models in anthropic? """
        return ["claude-3-5-sonnet-20240620"]
    

    def chat(self, message):
        if self.primer and len(self.messages) == 0:
            self.messages.append({"role": "user", "content": self.primer + "\n\n" + message})
        else:
            self.messages.append({"role": "user", "content": message})
        with self.client.messages.stream(
            max_tokens=1024,
            messages=self.messages,
            model=self.model,
                ) as stream:
            for text in stream.text_stream:
                yield text
        self.messages.append({"role": "assistant", "content": text})


    def new_chat(self, primer=None):
        self.messages = []
        if primer:
            self.primer = primer


if __name__ == "__main__": # pragma: no cover
    client = AnthropicClient(primer="Limit your response to 300 characters or less")
    for text in client.chat("Provide a list of 7 things I could do when I have a spare hour at home, which won't waste my time?"):
        print(text, end="", flush=True)
    print()
    print("---")
    
    for text in client.chat("out of those, which one would you recommend?"):
        print(text, end="", flush=True)
    print()
