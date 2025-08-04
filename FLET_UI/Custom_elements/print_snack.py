from flet import (Page, Text, SnackBar)

import sys
import os

# Add the parent directory to sys.path
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, parent_dir)

from Custom_log import DEBUG_log

def print_snack(page: Page, message: str = None):
    """
    Displays a snack bar with a message on the provided page.

    Args:
        page (Page): The Flet page where the snack bar will be displayed.
        message (str): The message to be displayed in the snack bar.
        translator (Translator): An optional Translator instance for translating the message.

    Returns:
        None
    """

    if message is None:
        message = "DEBUG"

    try:
        message_snack = SnackBar(Text(message), duration= 2000)
        page.overlay.append(message_snack)
        message_snack.open = True
        page.update()
        page.overlay.remove(message_snack)
    except AssertionError as e:
        DEBUG_log(f"Error displaying snack: {e}\n Message: {message}", level="ERROR")