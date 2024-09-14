from prompt_toolkit import PromptSession
from prompt_toolkit.history import FileHistory
from openai import OpenAI
from dotenv import load_dotenv
from collections import deque
from prompt_toolkit import print_formatted_text, HTML

from prompt_toolkit.styles import Style

style = Style.from_dict({
    'aaa': '#ff0066',
    'bbb': '#44ff00 italic',
})


load_dotenv()

client = OpenAI()

model = "gpt-4o-mini"

MAX_HISTORY = 30
chat_history = deque(maxlen=MAX_HISTORY)

def complete(prompt):
    # Include chat history in the messages
    messages = [
        {"role": "system", "content": "Please return the response using a plain text format (no markdown or code blocks or json or formatting unless specifically asked for)"},
    ]
    messages.extend(chat_history)
    messages.append({"role": "user", "content": prompt})

    response = client.chat.completions.create(
        model=model,
        messages=messages
    )
    assistant_message = response.choices[0].message.content
    
    # Add the new messages to chat history
    chat_history.append({"role": "user", "content": prompt})
    chat_history.append({"role": "assistant", "content": assistant_message})
    
    return assistant_message


def is_command(text):
    return text.strip().lower() in ['q', 'n', 'new', 'quit']

# Create a custom history class that filters out commands we don't want to save
class FilteredHistory(FileHistory):
    def store_string(self, string: str) -> None:
        # Don't store 'q', 'n', or 'new' commands
        if not is_command(string):
                super().store_string(string)

def main():
    # our_history = FileHistory(".example-history-file")
    
    our_history = FilteredHistory(".example-history-file")
    session = PromptSession(history=our_history)

    while True:
        try:
            user_message_count = sum(1 for msg in chat_history if msg["role"] == "user")
                # text = session.prompt(f"{model} ({user_message_count}) > ")
            text = session.prompt(HTML(f"<b><ansigray>{model}</ansigray></b> ({user_message_count+1}) > "))
            if text.strip() in ["q", "quit"]:
                break

            if text.strip() == "":
                continue

            if text.strip() in ["n", "new"]:
                chat_history.clear()
                print("Chat history cleared.")
                continue

            response = complete(text)
            print_formatted_text(HTML(f"<b><ansigray>{model}</ansigray></b>: <ansigreen>{response}</ansigreen>"))
        except KeyboardInterrupt:
            break
        except Exception as e:
            print_formatted_text(HTML(f"<b><ansired>Error: {e}</ansired></b>"))

    print("Bye!")



if __name__ == "__main__":
    main()