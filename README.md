![AZC logo](assets/azc_logo.png)

# azc - LLM Chat from the command-line

A command-line tool for interacting with LLMs.

![AZC screenshot](assets/recipe.gif)

# Why should you use this?

- If you're a command-line junkie, you don't need to switch to another tool to chat with your LLM
- One tool, multiple LLMs (OpenAI, Anthropic, Ollama, Gemini) - Why settle for one when you can have them all?
- Pay-as-you-go pricing for LLM providers (Cheaper in many cases)

# Features

- Multi-provider support
  - Ollama
  - OpenAI
  - Anthropic
  - Gemini
- Streaming responses (see response as it is being generated)
- Persistent command-line history (use up and down arrows to navigate)
- Chat history & reset (full discussion, start new chat)
- Switch provider and model (compare models and providers)
- Markdown output (nicely formatted headings, lists, tables, etc.)
- Command-line parameters (first prompt)

# Possible future features

- Support for more LLM providers
- Command-line completion (for providers and models)
- Support RTL languages
- Save output to file
- Patterns library (a-la fabrik)
- Upload files
- Aggregate responses from multiple providers
- Support more modes (image generation, transcription, etc.)
- Automated testing

# Installation

    pip install azc

# Running

    % azc
    azc> how tall is the eifel tower?
    openai:gpt-4o-mini: The Eiffel Tower is approximately 1,083 feet (330 meters) tall, including its antennas. The structure itself, without antennas, is about 1,063 feet (324 meters).
    azc> q
    Bye!
    %

    You can specify the first prompt as a command-line argument:

    % azc "what is the capital of the moon?"
    openai:gpt-4o-mini: The capital of the moon is called "New Moon".
    azc>

## Command-line parameters

- default parameter: first prompt
- `-d` / `--double-enter` - Press enter twice to submit - This is useful for those who want to use use multi-line prompts without pressing ctrl-j to add new line.
- `--provider` - The provider to use (coming soon)
- `--model` - The model to use (coming soon)

example:

    % azc "knock knock"
    providers configured: openai, ollama, anthropic, gemini
    using: openai:gpt-4o-mini
    type ? or h for help
    ...
    openai:gpt-4o-mini (1st message)
    Who's there?

    azc>

# Commands

- `q` or `exit` - exit the program
- `h` or `?` - show help
- `l` - list models
- `n` - start new chat
- `p` - Change provider
- `m` - Change model
- `ctrl-n` - new line

# Setup

You will need to configure at least one LLM API.

You should create a `.env` file which contains your API Key/s.

See `.env.sample` for a sample file

Here are the links to the API sign-up pages (or download in case of Ollama):

- [OpenAI](https://platform.openai.com/signup)
- [Anthropic](https://console.anthropic.com/)
- [Ollama](https://ollama.com/)
- [Gemini](https://ai.google.dev/gemini-api/docs)

# Contributing

Contributions are welcome! Please feel free to submit a PR.

# License

MIT
