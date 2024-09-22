import re

def number_to_ordinal(n):
    """
    Convert an integer n to its ordinal representation.

    Parameters:
    n (int): The number to convert.

    Returns:
    str: The ordinal representation of the number.
    """
    suffixes = {1: 'st', 2: 'nd', 3: 'rd'}
    if 10 <= n % 100 <= 20:
        suffix = 'th'
    else:
        suffix = suffixes.get(n % 10, 'th')
    return f"{n}{suffix}"


def remove_images_from_markdown(markdown_text):
    # Regex pattern to match Markdown image syntax
    image_pattern = r'!\[.*?\]\(.*?\)'
    # Remove all instances of image syntax from the text
    return re.sub(image_pattern, '', markdown_text)


if __name__ == "__main__": # pragma: no cover
    # demo
    import sys
    with open(sys.argv[1], 'r') as f:
        readme_content = f.read()

    # Remove images from the readme content
    readme_content_without_images = remove_images_from_markdown(readme_content)
    print(readme_content_without_images)