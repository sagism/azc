# from prompt_toolkit import PromptSession
# from prompt_toolkit.history import FileHistory
from openai import OpenAI
from dotenv import load_dotenv
from collections import deque
# from prompt_toolkit import print_formatted_text, HTML
from rich.console import Console
from rich.markdown import Markdown
import readline
import atexit
import os

histfile = os.path.join(os.path.expanduser("~"), ".chata_history")
try:
    readline.read_history_file(histfile)
    readline.set_history_length(1000)
except FileNotFoundError:
    pass

atexit.register(readline.write_history_file, histfile)


load_dotenv()

client = OpenAI()

"""
Note that at this point, I can either stream the response from the LLM, or I can print it all at once in markdown format,
but I can't do both, it just does not work right as I need to clear the console and reprint the markdown for each chunk,
and I have not figured out how to do that yet selectively
"""

console = Console()

# TODO: make this configurable
model = "gpt-4o-mini"

MAX_HISTORY = 30
chat_history = deque(maxlen=MAX_HISTORY)

def complete(prompt):
    messages = [
        {"role": "system", "content": "Please return the response using a plain text format (no markdown or code blocks or json or formatting unless specifically asked for)"},
    ]
    messages.extend(chat_history)
    messages.append({"role": "user", "content": prompt})

    stream = client.chat.completions.create(
        model=model,
        messages=messages,
        stream=True
    )

    assistant_message = ""
    for chunk in stream:
        content = chunk.choices[0].delta.content
        if content is not None:
            assistant_message += content
            yield content

    
    chat_history.append({"role": "user", "content": prompt})
    chat_history.append({"role": "assistant", "content": assistant_message})
    
    return assistant_message


def is_command(text):
    return text.strip().lower() in ['q', 'n', 'new', 'quit']


def print_markdown_stream(markdown_stream, gradual=False):
    """Print a streaming markdown response in a formatted way."""
    full_markdown = ""
    for chunk in markdown_stream:
        full_markdown += chunk

        if gradual:
            # Clear the console and reprint the full markdown
            console.clear()
            md = Markdown(full_markdown)
            console.print(md)
    
    if not gradual:
        console.print(Markdown(full_markdown))
    console.print()


def main():
    
    do_print_markdown = True
    gradual = False

    while True:
        try:
            user_message_count = sum(1 for msg in chat_history if msg["role"] == "user")
            prompt = f"[i]{model}[/i] [bold red]{user_message_count+1}[/] > "
            text = console.input(prompt)
            if text.strip() in ["q", "quit"]:
                break

            if text.strip() == "":
                continue

            if text.strip() in ["n", "new"]:
                chat_history.clear()
                console.print("Chat history cleared.")
                continue

            with console.status("Working..."):
                console.print(f"[i cyan]{model}:[/]")
                response = complete(text)

                if (do_print_markdown):
                    print_markdown_stream(response, gradual=gradual)
                else:
                    for chunk in response:
                        console.print(f"{chunk}", end="")
                    console.print()

        except KeyboardInterrupt:
            break
        except Exception as e:
            console.log(f"[red]Error: {e}[/]")

    console.print("[green]Bye![/]")



if __name__ == "__main__":
    main()