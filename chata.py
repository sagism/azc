from prompt_toolkit import PromptSession
from prompt_toolkit.history import FileHistory
from openai import OpenAI
from dotenv import load_dotenv


load_dotenv()

client = OpenAI()

model = "gpt-4o-mini"

def complete(prompt):
    response = client.chat.completions.create(
    model=model,
    messages=[
        {"role": "system", "content": "Please return the response using a plain text format (no markdown or code blocks or json or formatting unless specifically asked for)"},
        {"role": "user", "content": prompt},
    ]
    )
    return response.choices[0].message.content

def main():
    our_history = FileHistory(".example-history-file")

    session = PromptSession(history=our_history)

    while True:
        text = session.prompt("> ")
        if text == "q":
            break
        response = complete(text)
        print(f"{model}: {response}")


    print("Goodbye!")

if __name__ == "__main__":
    main()