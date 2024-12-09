![AZC logo](assets/azc_logo.png)

# azc - LLM Chat from the command-line

A command-line tool for interacting with LLMs.

![AZC screenshot](assets/sample.gif)

# Why should you use this?

- If you're a command-line junkie, you don't need to switch to another tool to chat with your LLM
- One tool, multiple LLMs (OpenAI, Anthropic, Ollama, Gemini...) - Why settle for one when you can have them all?
- Pay-as-you-go pricing for LLM providers (Cheaper in many cases)

# Features

- Multi-provider support
  - Ollama
  - OpenAI
  - Anthropic
  - Gemini
  - Grok
- Streaming responses (see response as it is being generated)
- Persistent command-line history (use up and down arrows to navigate)
- Chat history & reset (full discussion, start new chat)
- Switch provider and model (compare models and providers)
- Markdown output (nicely formatted headings, lists, tables, etc.)
- Command-line parameters (first prompt)

# Possible future features

- Support more LLM providers (Perplexity, Groq...)
- Support RTL languages
- Save output to file
- Patterns library (a-la fabric)
- Upload files
- Aggregate responses from multiple providers
- Support more modes (image generation, transcription, etc.)
- Track total cost of API calls
- Add to homebrew

# Installation

    pip install azc

if you want to make it available system-wide (any folder, without having to activate your python environment), you can install it system-wide:

    echo 'alias azc="$HOME/projects/azc/env/bin/azc"' >> ~/.bashrc

- Replace `~/.bashrc` with the shell you are using (zsh, bash, etc.)
- Replace `$HOME/projects/azc/env/bin/azc` with the path to the azc executable
- On Windows, you can add the path to your PATH environment variable (ask your nearest LLM for more details)

# Running

    % azc
    azc> how tall is the eiffel tower?
                                      ollama:llama3.1:latest (1st message)
      The Eiffel Tower stands at an impressive height of:

      • 324 meters (1,063 feet) tall, including its antenna.
      • 302.9 meters (994.7 feet) tall, excluding its antenna.

      It was the world's tallest man-made structure when it was first built for the 1889 World's Fair in
      Paris.

    azc> q
    👋 Bye
    %

You can specify the first prompt as a command-line argument:

    % azc -b "What is the capital of Panama?"
    The capital of Panama is Panama City.
    %

## Command-line parameters

| Parameter               | Description                                                                                                                        |
| ----------------------- | ---------------------------------------------------------------------------------------------------------------------------------- |
| (default)               | First prompt                                                                                                                       |
| `-d` / `--double-enter` | Press enter twice to submit - This is useful for those who want to use multi-line prompts without pressing ctrl-j to add new line. |
| `-b` / `--batch`        | Exit after the first response                                                                                                      |
| `-v` / `--verbose`      | Print verbose output                                                                                                               |
| `-p` / `--provider`     | The provider to use (e.g. `openai` or `ollama`). Abbreviations allowed, like `op` for `openai`                                     |
| `-m` /`--model`         | The model to use. Abbreviations allowed, like `tu` for `gpt-3.5-turbo`                                                             |

## Commands

| Command       | Description                                                                    |
| ------------- | ------------------------------------------------------------------------------ |
| `q` or `exit` | Exit the program                                                               |
| `h` or `?`    | Show help                                                                      |
| `l`           | List models                                                                    |
| `n`           | Start new chat                                                                 |
| `p`           | Change provider. `p ` - (`p` followed by a space) trigger auto-completion menu |
| `m`           | Change model                                                                   |
| `ctrl-n`      | New line                                                                       |

# Setup

You will need to configure at least one LLM API.

You should create a `.env` file which contains your API Key/s.
The `.env` file should be located in home directory, either directly under `$HOME` or under `$HOME/.config/`, the latter taking precedence.
See `.env.sample` for a sample `.env` file, with the expected environment variables' names. Remove those that are not relevant to you.

Here are the links to the API sign-up pages (or download in case of Ollama):

- [OpenAI](https://platform.openai.com/signup)
- [Anthropic](https://console.anthropic.com/)
- [Ollama](https://ollama.com/)
- [Gemini](https://ai.google.dev/gemini-api/docs)
- [Grok](https://docs.x.ai/api/integrations)

You can configure the default models you want to use in `azc_config.json`.
This file is expected to be found under `~/.config/azc_config.json` or `~/.azc_config.json` if you don't have a `~/.config` folder.

# Limitations

- Streaming updates are limited to screen height (after that it displays ellipsis and will update the display only when the response is complete)
- No support for RTL languages

# Contributing

Contributions are welcome! Please feel free to submit a PR.

To run in development:

    % python -m az.az

# License

MIT
