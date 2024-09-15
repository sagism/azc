MARKDOWN = """
# This is an h1

Rich can do a pretty *decent* job of rendering markdown.

1. This is a list item
2. This is another list item

and this is a [link](https://rich.readthedocs.io/en/latest/introduction.html)

and a table

| Column 1 | Column 2 | Column 3 |
| -------- | -------- | -------- |
| Cell 1   | Cell 2   | Cell 3   |
| Cell 4   | Cell 5   | Cell 6   |
| Cell 7   | Cell 8   | Cell 9   |
"""

import time
from rich.console import Console
from rich.markdown import Markdown

console = Console()

def print_markdown_stream(markdown_stream):
    """Print a streaming markdown response in a formatted way."""
    full_markdown = ""
    for chunk in markdown_stream:
        full_markdown += chunk
        # Clear the console and reprint the full markdown
        console.clear()
        md = Markdown(full_markdown)
        console.print(md)
    console.print()


# Example usage:
def mock_markdown_stream():
    for line in MARKDOWN.splitlines():
        yield line + "\n"
        time.sleep(0.2)


print_markdown_stream(mock_markdown_stream())
