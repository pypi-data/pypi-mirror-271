"""
file_utils.py: A module providing utility functions for file operations.

This module provides functions for performing various file operations with additional features such as prompting the user before overwriting existing files.

Functions:
    - copy_file_with_prompt: Copy a file from source to destination, prompting the user if the destination file already exists.
"""

import os
import shutil

def copy_file_with_prompt(src_file, dst_file, force=False):
    """
    Copy a file from source to destination, prompting the user if the destination file already exists.

    Args:
        src_file (str): The path to the source file.
        dst_file (str): The path to the destination file.
        force (bool, optional): If True, overwrite the destination file without prompting. Defaults to False.

    Returns:
        bool: True if the file was successfully copied, False otherwise.
    """
    if os.path.exists(dst_file) and not force:
        overwrite = input(f"The file '{dst_file}' already exists. Do you want to overwrite it? (yes/no): ")
        if overwrite.lower() != 'yes':
            print("Operation canceled.")
            return False

    try:
        shutil.copy(src_file, dst_file)
        print(f"File '{src_file}' copied to '{dst_file}' successfully.")
        return True
    except Exception as e:
        print(f"Error copying file '{src_file}' to '{dst_file}': {e}")
        return False
