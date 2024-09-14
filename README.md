# LLM Chat from the command-line

Right now only supports OpenAI Completion API, but later will support more...

# Installation

    pip install chata

# Running

    % python chata.py
    > how tall is the eifel tower?
    gpt-4o-mini: The Eiffel Tower is approximately 1,083 feet (330 meters) tall, including its antennas. The structure itself, without antennas, is about 1,063 feet (324 meters).
    > q
    Bye!
    % 


# Setup

You will need to configure an LLM API.

For example, if using the OpenAPI Completion API, you should create a .env file which contains your API Key.
    
See `.env.sample` for a sample file
