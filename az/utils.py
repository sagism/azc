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