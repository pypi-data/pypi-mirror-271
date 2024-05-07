"""
writer.py: A module providing utility functions for writing files.

This module provides functions to write content to files with additional features such as prompting the user before overwriting existing files.

Functions:
    - write_file_with_prompt: Write content to a file, prompting the user if the file already exists.
"""

import os

def write_file_with_prompt(file_path, content, force=False):
    """
    Write content to a file, prompting the user if the file already exists.

    Args:
        file_path (str): The path to the file.
        content (str): The content to write to the file.
        force (bool, optional): If True, overwrite the file without prompting. Defaults to False.

    Returns:
        bool: True if the file was successfully written, False otherwise.
    """
    if os.path.exists(file_path) and not force:
        overwrite = input(f"The file '{file_path}' already exists. Do you want to overwrite it? (yes/no): ")
        if overwrite.lower() != 'yes':
            print("Operation canceled.")
            return False

    try:
        with open(file_path, 'w') as file:
            file.write(content)
        print(f"File '{file_path}' successfully written.")
        return True
    except Exception as e:
        print(f"Error writing to file '{file_path}': {e}")
        return False
