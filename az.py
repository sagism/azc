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

from az.ollama_provider import OllamaClient
from az.openai_provider import OpenAIClient
from az.anthropic_provider import AnthropicClient  


from prompt_toolkit import PromptSession
from prompt_toolkit.patch_stdout import patch_stdout
from prompt_toolkit.formatted_text import HTML
from prompt_toolkit.history import FileHistory
import readline # needed for prompt editing




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

console.print('providers configured:', ', '.join(providers))

def primer():
    columns, rows = shutil.get_terminal_size()
    # single screen is better...
    return f"please limit your response to {rows-4} lines at most)"


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
        return OllamaClient(primer=primer())
    elif provider_full_name == 'openai':
        return OpenAIClient(primer=primer())
    elif provider_full_name == 'anthropic':
        return AnthropicClient(primer=primer())


def is_command(string: str) -> bool:
    return string.strip().lower() in ('exit', 'quit', 'q', 'p', 'l', 'm', 'p', 'n', 'h', '?', '')

class FilteredHistory(FileHistory):
    """
    This class is a custom history class that filters out commands we don't want to save
    """
    def store_string(self, string: str) -> None:
        if not is_command(string):
                super().store_string(string)


def help():
    return """

    | Command | Description |
    |---------|-------------|
    | l       | list models |
    | n       | new chat    |
    | ? or h  | help        |
    | m       | change model |
    | p       | change provider |

    """

def main():
    if len(providers) == 0:
        console.print('no providers found, exiting, please set one of the following: OPENAI_API_KEY, OLLAMA_URL, ANTHROPIC_API_KEY in a .env file')
        return

    provider_name = providers[0]
    client = provider_factory(provider_name)
    console.print('using: ', client)


    # Check if a command-line argument was provided
    initial_prompt = None
    if len(sys.argv) > 1:
        initial_prompt = ' '.join(sys.argv[1:])

    our_history = FilteredHistory(".example-history-file")
    session = PromptSession(history=our_history)

    try:
        while True:
            # If there's an initial prompt, process it first
            if initial_prompt:
                user_input = initial_prompt
            else:
                # Get user input using prompt_toolkit
                with patch_stdout():
                    user_input = session.prompt(
                        HTML(f'<ansicyan>az></ansicyan> '),
                        multiline=False,
                        is_password=False
                    )

            if user_input.strip().lower() == '':
                # Some people like to press enter to get a new line
                continue

            if user_input.strip().lower() in ('exit', 'quit', 'q'):
                break

            if user_input.strip().lower() in ('l'):
                console.print(Markdown('\n' + '\n  - '.join(client.list_models() )))
                continue

            if user_input.strip().lower() in ('n'):
                client.new_chat()
                continue

            if user_input.strip().lower() in ('h', '?'):
                console.print(Markdown(help()))
                continue

            if user_input.strip().lower() in ('m'):
                model = session.prompt(
                    HTML(f'<ansicyan>model: </ansicyan> '),
                    multiline=False,
                    is_password=False
                )
                client.model = model
                continue

            if user_input.strip().lower() in ('p'):
                provider_name = session.prompt(
                    HTML(f'<ansicyan>provider: </ansicyan> '),
                    multiline=False,
                    is_password=False
                )
                client = provider_factory(provider_name)
                console.print(f'using provider: {client.provider} in new session')
                continue


            assistant_panel = Panel(
                Align.left(""),
                title="Assistant",
                style="yellow",
                expand=True,
                box=EMPTY
            )

            current_message = ""

            with Live(assistant_panel, console=console, refresh_per_second=2, vertical_overflow='ellipsis') as live:
                for chunk in client.chat(user_input):
                    current_message += chunk
                    assistant_panel = Panel(
                        Align.left(Markdown(current_message)),
                        title="Assistant",
                        style="yellow",
                        expand=True,
                        border_style="none",
                        box=EMPTY
                    )
                    live.update(assistant_panel)

    except KeyboardInterrupt:
        pass
    finally:
        console.print(":wave: [italic]Bye[/]")

if __name__ == "__main__":
    main()


