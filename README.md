# LLM Chat from the command-line

Right now only supports OpenAI Completion API, but later will support more...

Features:

    - Persistent command-line history
    - Chat history & reset
    - Multi-provider support
        - Ollama
        - OpenAI

# Possible future features

    - Support for other LLM providers
    - Support RTL languages
    - Save output to file

# Installation

    pip install chata

# Running

    % az
    > how tall is the eifel tower?
    gpt-4o-mini: The Eiffel Tower is approximately 1,083 feet (330 meters) tall, including its antennas. The structure itself, without antennas, is about 1,063 feet (324 meters).
    > q
    Bye!
    %

    Use `q` to exit
    Use `p` to set the provider (you can use a partial name)
    Use `l` to list the models for the selected provider
    Use `m` to set the model (you can use a partial name)

    You can specify the first prompt as a command-line argument:

    % az "what is the capital of the moon?"
    gpt-4o-mini: The capital of the moon is called "New Moon".
    >

# Setup

You will need to configure an LLM API.

For example, if using the OpenAPI Completion API, you should create a .env file which contains your API Key.

See `.env.sample` for a sample file
