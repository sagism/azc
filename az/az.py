# chat_app.py

import sys
import os
import shutil
import argparse


from dotenv import load_dotenv

# a mix of rich and prompt_toolkit seem to hit the sweet spot for terminal UI interactivity
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.align import Align
from rich.live import Live
from rich.box import Box
from prompt_toolkit import PromptSession
from prompt_toolkit.patch_stdout import patch_stdout
from prompt_toolkit.formatted_text import HTML
from prompt_toolkit.history import FileHistory
from prompt_toolkit.completion import Completer, Completion
from prompt_toolkit.key_binding import KeyBindings

import readline # needed for prompt editing

from .utils import number_to_ordinal
from .config import load_config

# Providers
from .ollama_provider import OllamaClient
from .openai_provider import OpenAIClient
from .anthropic_provider import AnthropicClient
from .gemini_provider import GeminiClient

config = load_config()

bindings = KeyBindings()

def is_command(string: str) -> bool:
    if string.strip().lower() in ('exit', 'quit', 'q', 'p', 'l', 'm', 'p', 'n', 'h', '?', ''): return True
    elif string.strip().startswith("p "): return True
    else: return False


# Bind 'Control+n' to insert a newline
@bindings.add('c-n')
def insert_newline(event):
    event.current_buffer.insert_text('\n')


# An empty box border makes it easier to copy and paste.
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
if 'GEMINI_API_KEY' in os.environ:
    providers.append('gemini')

# provider_completer = WordCompleter([f"p {provider}" for provider in providers], ignore_case=True)

class CommandsCompleter(Completer):
    """
    This completer handles the 'p' command for changing provider
    """
    def get_completions(self, document, complete_event):
        text = document.current_line
        if text.startswith('p '):   
            for provider in providers:
                yield Completion(
                f'p {provider}', start_position=-1000,
                display=HTML(f'{provider}'),
                style='bg:ansiyellow')
        
completer = CommandsCompleter()

console.print('providers configured: [yellow]' + ', '.join(providers) + '[/]')

def primer():
    _, rows = shutil.get_terminal_size()
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
        return OpenAIClient(config, primer=primer())
    elif provider_full_name == 'anthropic':
        return AnthropicClient(config, primer=primer())
    elif provider_full_name == 'gemini':
        return GeminiClient(config, primer=primer())




class FilteredHistory(FileHistory):
    """
    This class is a custom history class that filters out commands we don't want to save
    """
    def store_string(self, string: str) -> None:
        if not is_command(string):
                super().store_string(string)


def help():
    return """

Just type your message and press enter to start a chat.

| Command | Description |
|---------|-------------|
| l       | List models |
| n       | New chat ( )   |
| ? or h  | Help (this screen) |
| m       | Change model |
| p       | Change provider (p and space trigger autocomplete) |
| ctrl-n  | New line |
"""

def main(initial_prompt=None):
    if len(providers) == 0:
        console.print('no providers found, exiting, please set one of the following: OPENAI_API_KEY, OLLAMA_URL, ANTHROPIC_API_KEY, GEMINI_API_KEY in a .env file')
        return
    
    parser = argparse.ArgumentParser(description="Chat with an AI assistant")
    parser.add_argument("-d", "--double-enter", action="store_true", help="Enable 'press enter twice to submit' mode")
    parser.add_argument("initial_prompt", nargs='?', help="Initial prompt (if provided without a flag)")
    args = parser.parse_args()
    initial_prompt = args.initial_prompt

    if args.double_enter:
        console.print("type <enter> twice to submit...")
        @bindings.add('enter')
        def _(event):
            buffer = event.current_buffer
            # print(f'handling enter [{buffer.document.text}]')
            accepted = False
            if buffer.document.text.strip() == '':
                # print("empty")
                accepted = True
            elif is_command(buffer.document.text):
                # print("is command")
                accepted = True
            elif buffer.document.text.endswith('\n') and buffer.document.is_cursor_at_the_end:
                # print("dbl-newline")
                # Submit if there's at least two newlines and cursor is at the end
                accepted = True
            else:
                # print("newline")
                # buffer.insert_text('\n')
                accepted = False
            if accepted:
                buffer.validate_and_handle()
            else:
                buffer.insert_text('\n')

    provider_name = providers[0] # dumb default. should probably let user set it
    client = provider_factory(provider_name)
    console.print(f'using: [green]{client}[/]')
    console.print('[magenta]type ? or h for help[/]')


    def bottom_toolbar():
        return HTML(f' Using <b>{client}</b> ({number_to_ordinal(client.n_user_messages()+1)} message)')


    our_history = FilteredHistory(".example-history-file")
    session = PromptSession(history=our_history)


    done=False

    try:
        while not done:
            # If there's an initial prompt, process it first
            if initial_prompt:
                user_input = initial_prompt
                initial_prompt = None
            else:
                # Get user input using prompt_toolkit
                with patch_stdout():
                    user_input = session.prompt(
                        HTML(f'<ansicyan>azc></ansicyan> '),
                        completer=completer,
                        bottom_toolbar=bottom_toolbar,
                        key_bindings=bindings
                    )

            if user_input.strip().lower() == '':
                # Some people like to press enter to get a new line
                continue

            if user_input.strip().lower() in ('exit', 'quit', 'q'):
                break

            if user_input.strip().lower() in ('l'):
                console.print(Markdown('  - ' + '\n  - '.join(client.list_models())))
                continue

            if user_input.strip().lower() in ('n'):
                client.new_chat()
                continue

            if user_input.strip().lower() in ('h', '?'):
                console.print(Markdown(help()))
                continue

            if user_input.strip().lower() in ('m'):
                model = session.prompt(
                    HTML(f'<ansicyan>model (partial name okay): </ansicyan> '),
                    multiline=False,
                    is_password=False
                )
                client.model = model
                continue

            if user_input.startswith('p '):
                provider_name = user_input.split(' ')[1]
                try:
                    client = provider_factory(provider_name)
                    console.print(f'using: {client} (new chat)')
                except ValueError as e:
                    console.print(f'[red]error: {e}[/]')
                continue

            title = f"{client} ({number_to_ordinal(client.n_user_messages()+1)} message)"

            assistant_panel = Panel(
                Align.left(""),
                title=title,
                style="yellow",
                expand=True,
                box=EMPTY
            )

            current_message = ""

            with Live(assistant_panel, console=console, refresh_per_second=2, vertical_overflow='ellipsis') as live:
                console.print(f'...')
                for chunk in client.chat(user_input):
                    current_message += chunk
                    assistant_panel = Panel(
                        Align.left(Markdown(current_message)),
                        title=title,
                        style="yellow",
                        expand=True,
                        border_style="none",
                        box=EMPTY
                    )
                    live.update(assistant_panel)

    except KeyboardInterrupt:
        done = True
    finally:
        console.print(":wave: [italic]Bye[/]")

if __name__ == "__main__":
    main()


