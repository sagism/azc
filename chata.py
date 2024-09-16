# chat_app.py

import sys
import os
import shutil

from dotenv import load_dotenv
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.align import Align
from rich.live import Live
from rich.box import Box
from openai import OpenAI
from prompt_toolkit import PromptSession
from prompt_toolkit.patch_stdout import patch_stdout
from prompt_toolkit.formatted_text import HTML
from prompt_toolkit.history import FileHistory
import readline # needed for prompt editing

"""
This is a chat app that allows you to chat with multiple providers

You need to configure providers in the .env file

it supports:

- openai
- ollama
- anthropic

use the 'p' key to change providers
use the 'q' key to quit

"""



# An empty box border makes it easier to copy and paste the code.
EMPTY: Box = Box(
    "    \n"
    "    \n"
    "    \n"
    "    \n"
    "    \n"
    "    \n"
    "    \n"
    "    \n",
    ascii=True,
)

load_dotenv()

# Initialize the console
console = Console()

providers = []
if 'OPENAI_API_KEY' in os.environ:
    providers.append('openai')
if 'OLLAMA_URL' in os.environ:
    providers.append('ollama')
if 'ANTHROPIC_API_KEY' in os.environ:
    providers.append('anthropic')

console.print('providers:', providers)


def provider_factory(provider_hint):
    provider_found = False

    for provider_name in providers:
        if provider_hint in provider_name:
            provider_full_name = provider_name
            provider_found = True
            break

    if not provider_found:
        raise ValueError(f"Cannot find provider with <{provider_hint}>")
    
    if provider_full_name == 'ollama':
        model = "llama3.1:latest"
        return OpenAI(
            base_url=os.environ['OLLAMA_URL'],
            api_key='ollama',  # required, but unused in your local setup
        ), provider_full_name,model
    elif provider_full_name == 'openai':
        model = 'gpt-4o-mini'
        return OpenAI(), provider_full_name, model
    else:
        raise ValueError(f"Invalid provider: {provider_full_name}")


def is_command(string: str) -> bool:
    return string.strip().lower() in ('exit', 'quit', 'q', 'p', 'l', 'm', 'p', '')

class FilteredHistory(FileHistory):
    """
    This class is a custom history class that filters out commands we don't want to save
    """
    def store_string(self, string: str) -> None:
        if not is_command(string):
                super().store_string(string)

def primer():
    columns, rows = shutil.get_terminal_size()
    # single screen is better...
    return [{"role": "system", "content": f"please limit your response to {rows-4} lines at most)"}]


def list_models(client):
    console.print('models: ')
    model_names = [ m.id for m in client.models.list() ]
    console.print(Markdown(' \n ' + '\n - '.join(model_names)))
    console.print('')



def main():
    if len(providers) == 0:
        console.print('no providers found, exiting')
        return

    provider_name = providers[0]
    client, provider_name, model = provider_factory(provider_name)
    console.print('using provider: ', provider_name)

    # Initialize the conversation with a system message
    messages = primer()

    # Check if a command-line argument was provided
    if len(sys.argv) > 1:
        initial_prompt = ' '.join(sys.argv[1:])
        messages.append({"role": "user", "content": initial_prompt})
        console.print(f"Initial prompt: {initial_prompt}")

    our_history = FilteredHistory(".example-history-file")
    session = PromptSession(history=our_history)

    try:
        while True:
            # If there's an initial prompt, process it first
            if messages and messages[-1]["role"] == "user":
                user_input = messages.pop()["content"]
            else:
                # Get user input using prompt_toolkit
                with patch_stdout():
                    user_input = session.prompt(
                        HTML(f'<ansicyan>{model}: </ansicyan> '),
                        multiline=False,
                        is_password=False
                    )

            if user_input.strip().lower() == '':
                # Some people like to press enter to get a new line
                continue

            if user_input.strip().lower() in ('exit', 'quit', 'q'):
                break

            if user_input.strip().lower() in ('l'):
                list_models(client)
                continue

            if user_input.strip().lower() in ('m'):
                model = session.prompt(
                    HTML(f'<ansicyan>model: </ansicyan> '),
                    multiline=False,
                    is_password=False
                )
                continue

            if user_input.strip().lower() in ('p'):
                provider_name = session.prompt(
                    HTML(f'<ansicyan>provider: </ansicyan> '),
                    multiline=False,
                    is_password=False
                )
                client, provider_name, model = provider_factory(provider_name)
                console.print(f'using provider: {provider_name} in new session')
                messages = primer()
                continue

            messages.append({"role": "user", "content": user_input})

            current_message = ""

            assistant_panel = Panel(
                Align.left(Markdown(current_message)),
                title="Assistant",
                style="yellow",
                expand=True,
                box=EMPTY
            )

            with Live(assistant_panel, console=console, refresh_per_second=2, vertical_overflow='ellipsis') as live:
                response_stream = client.chat.completions.create(
                    model=model,
                    messages=messages,
                    stream=True
                )
                for chunk in response_stream:
                    delta = chunk.choices[0].delta
                    content = getattr(delta, 'content', '')
                    if content:
                        current_message += content
                        # Update the assistant's panel with new content
                        assistant_panel = Panel(
                            Align.left(Markdown(current_message)),
                            title="Assistant",
                            style="yellow",
                            expand=True,
                            border_style="none",
                            box=EMPTY
                        )
                        live.update(assistant_panel)

            messages.append({"role": "assistant", "content": current_message})
    except KeyboardInterrupt:
        pass
    finally:
        console.print(":wave: [italic]Bye[/]")

if __name__ == "__main__":
    main()


