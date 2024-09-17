""" Base class for LLM providers """

class LLMProvider:

    def __init__(self, primer=None, model=None):
        self.provider = None
        self.model = model
        self.messages = []
        self.primer = None

    def list_models(self):
        """ List all models available for this provider """
        return []

    def chat(self, message):
        """ Chat with the LLM provider 
        return a generator that yields the response text 
        """
        pass
    
    @property
    def model(self):
        return self._model

    @model.setter
    def model(self, value):
        for m in self.models:
            if value in m:
                self._model = m
                return
        raise ValueError(f"Model {value} not found")
    
    def new_chat(self, primer=None):
        """ Create a new chat (erase messages history)
        Note that the semantics of the primer is that we reuse the original primer
        when not specified here.
        """
        self.messages = []
        if primer:
            self.primer = primer
        if self.primer:
            # Default is to use OpenAI system prompt
            self.messages.append({"role": "system", "content": self.primer})

    def n_user_messages(self):
        """ Number of user messages in the history """
        return len([m for m in self.messages if m['role'] == 'user'])

    def __str__(self):
        return f"{self.provider}:{self.model}"
    
    def __repr__(self):
        return f"{self.provider}:{self.model}"