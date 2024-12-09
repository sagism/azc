# chat_app.py

import sys
import os
import shutil
import argparse

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

from az.utils import number_to_ordinal
from az.config import load_config, default_model, default_provider

# Providers
from az.ollama_provider import OllamaClient
from az.openai_provider import OpenAIClient
from az.anthropic_provider import AnthropicClient
from az.gemini_provider import GeminiClient
from az.grok_provider import GrokClient

HISTORY_FILE_NAME = os.path.expanduser("~/.config/.azc_history" if os.path.exists(os.path.expanduser("~/.config")) else "~/.azc_history")

config = load_config()

bindings = KeyBindings()

def is_command(string: str) -> bool:
    if string.strip().lower() in ('exit', 'quit', 'q', 'p', 'l', 'm', 'p', 'n', 'h', 'r', '?', ''): return True
    elif string.strip().startswith("p "): return True
    else: return False


def get_input():
    # added so we can override input for testing
    return None


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

# Initialize the console
console = Console()

# this is done by the providers so it's not needed here
# load_dotenv(os.path.expanduser("~/.config/.env" if os .path.exists(os.path.expanduser("~/.config")) else "~/.env"))


providers = []
if 'OPENAI_API_KEY' in os.environ:
    providers.append('openai')
if 'OLLAMA_URL' in os.environ:
    providers.append('ollama')
if 'ANTHROPIC_API_KEY' in os.environ:
    providers.append('anthropic')
if 'GEMINI_API_KEY' in os.environ:
    providers.append('gemini')
if 'XAI_API_KEY' in os.environ:
    providers.append('grok')


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
    elif provider_full_name == 'grok':
        return GrokClient(config, primer=primer())



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
| r       | Refresh models |
| n       | New chat ( )   |
| ? or h  | Help (this screen) |
| m       | Change model |
| p provider_name | Change provider (p and space trigger autocomplete) |
| ctrl-n  | New line |
"""



def main(initial_prompt=None):
    if len(providers) == 0:
        console.print('no providers found, exiting, please set one of the following: OPENAI_API_KEY, OLLAMA_URL, ANTHROPIC_API_KEY, GEMINI_API_KEY in a .env file')
        return
    
    parser = argparse.ArgumentParser(description="Chat with an AI assistant")
    parser.add_argument("-p", "--provider", help="The provider to use, e.g. 'openai' or 'ollama'. Abbreviations allowed, like 'op' for 'openai'")
    parser.add_argument("-m", "--model", help="The model to use")
    parser.add_argument("-d", "--double-enter", action="store_true", help="Enable 'press enter twice to submit' mode")
    parser.add_argument("-b", "--batch", action="store_true", help="Not interactive, just do one chat and exit")
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose output")
    parser.add_argument("initial_prompt", nargs='?', help="Initial prompt (if provided without a flag)")
    args = parser.parse_args()
    initial_prompt = args.initial_prompt

    if args.verbose:
        console.print('providers configured: [yellow]' + ', '.join(providers) + '[/]')

    if args.double_enter:
        console.print("type <enter> twice to submit...")
        @bindings.add('enter')
        def _(event):
            buffer = event.current_buffer
            accepted = False
            if buffer.document.text.strip() == '':
                accepted = True
            elif is_command(buffer.document.text):
                accepted = True
            elif buffer.document.text.endswith('\n') and buffer.document.is_cursor_at_the_end:
                accepted = True
            else:
                accepted = False
            if accepted:
                buffer.validate_and_handle()
            else:
                buffer.insert_text('\n')



    provider_name = args.provider if args.provider else default_provider()
    provider_name = provider_name if provider_name else providers[0]
    
    client = provider_factory(provider_name)

    if args.model:
        client.model = args.model
    
    if args.verbose:
        console.print(f'using: [green]{client}[/]')
        console.print('[magenta]type ? or h for help[/]')

    def bottom_toolbar():
        return HTML(f' Using <b>{client}</b> ({number_to_ordinal(client.n_user_messages()+1)} message)     <ansicyan>enter ? or h for help</ansicyan> ')

    our_history = FilteredHistory(HISTORY_FILE_NAME)
    session = PromptSession(history=our_history, input=get_input())

    done=False
    
    try:
        while not done:
            # If there's an initial prompt, process it first
            if initial_prompt:
                user_input = initial_prompt
                initial_prompt = None
                if args.batch:
                    done=True
            else:
                # Get user input using prompt_toolkit
                with patch_stdout():
                    try:
                        user_input = session.prompt(
                            HTML(f'<ansicyan>azc></ansicyan> '),
                            completer=completer,
                            bottom_toolbar=bottom_toolbar,
                            key_bindings=bindings
                        )
                    except EOFError:
                        done = True
                        break


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

            if user_input.strip().lower() in ('r'):
                client.refresh_models()
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

            title = f"{client} ({number_to_ordinal(client.n_user_messages()+1)} message)" if not args.batch else None

            assistant_panel = Panel(
                Align.left(""),
                title=title,
                style="yellow",
                expand=True,
                box=EMPTY
            )

            current_message = ""

            # Note that vertical_overflow="visible" causes realtime updates of rendered markdown beyond the full window height,
            # but it leaves a trail of partially rendered markdown behind when new content is added, hence it is not used
            with Live(assistant_panel, console=console, refresh_per_second=2, vertical_overflow='ellipsis') as live:
                if args.double_enter:
                    console.print(f'...')
                for chunk in client.chat(user_input):
                    current_message += chunk
                    new_panel = Panel(
                        Align.left(Markdown(current_message)),
                        title=title,
                        style="yellow",
                        expand=True,
                        border_style="none",
                        box=EMPTY
                    )
                    live.update(new_panel, refresh=False)

    except KeyboardInterrupt:
        done = True
    finally:
        if not args.batch:
            console.print(":wave: [italic]Bye[/]")

if __name__ == "__main__": # pragma: no cover
    main()


