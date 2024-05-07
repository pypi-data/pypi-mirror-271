"""
banner: A utility module for printing formatted banners in the console.

This module provides a function for printing banners with customizable text, width, border character, alignment,
and newline options.

Example:
    ```
    from banner import print_banner

    # Print a centered banner with default width and border character
    print_banner("Hello, World!")

    # Print a left-aligned banner with custom width and border character
    print_banner("Welcome", width=60, border_char="-", alignment="left")

    # Print a right-aligned banner without newline
    print_banner("Goodbye", width=50, border_char="*", alignment="right", newline=False)
    ```
"""

def print_banner(text: str, width: int = 80, border_char: str = "#", alignment: str = 'center', newline: bool = True):
    """
    Print a formatted banner with the specified text.

    Args:
        text (str): The text to display in the banner.
        width (int): The width of the banner. Default is 80 characters.
        border_char (str): The character used for the border of the banner. Default is "#".
        alignment (str): The alignment of the text within the banner. Options: 'left', 'center', 'right'. Default is 'center'.
        newline (bool): Whether to print a newline before and after the banner. Default is True.
    """
    border = border_char * width
    if alignment == 'center':
        padding = (width - len(text) - 2) // 2
        banner_text = f"{border_char}{' ' * padding}{text}{' ' * padding}{border_char}"
    elif alignment == 'left':
        banner_text = f"{border_char} {text}{' ' * (width - len(text) - 2)} {border_char}"
    elif alignment == 'right':
        banner_text = f"{border_char}{' ' * (width - len(text) - 2)}{text} {border_char}"
    else:
        raise ValueError("Invalid alignment. Options: 'left', 'center', 'right'.")

    if newline:
        print(border)
    print(banner_text)
    if newline:
        print(border)
