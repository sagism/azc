from prompt_toolkit import PromptSession
from rich.console import Console


def main():
    session = PromptSession()
    console = Console()
    result = session.prompt("Enter a number: ")
    console.print(result)


if __name__ == "__main__":
    main()  