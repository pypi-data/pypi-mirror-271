from typing import List, Literal, Tuple, Union
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.shortcuts import input_dialog, yes_no_dialog, checkboxlist_dialog
from getpass import getpass

def dialog(message: str = None, dialog_type: Literal["input", "confirm", "checkbox"] = "input", title: str = "Dialog", choices: List[Tuple[str, bool]] = None) -> Union[str, bool, List[Tuple[str, bool]]]:
    """
    A function for handling user inputs in the terminal using dialogs.

    Example:
        ```python
        import zyx
        zyx,dialog(message="What is your name?", title="Input", dialog_type="input")
        zyx.dialog(message="Are you sure?", dialog_type="confirm")
        zyx.dialog(message="Choose colors:", choices=[("Red", True), ("Green", False), ("Blue", False)], dialog_type="checkbox")
        ```

    Args:
        message (str): Message to be displayed in the terminal.
        title (str): Title of the dialog box.
        dialog_type (str): Type of dialog to display. Options: 'input', 'confirm', 'checkbox'.
        choices (List[Tuple[str, bool]]): A list of tuples for the checkbox options. Only required for 'checkbox' dialog_type.
                                          Each tuple should contain a string and a boolean value.
    """
    if dialog_type == "input":
        if message and title:
            return input_dialog(title=title, text=message).run()
        else:
            print("'title' and 'message' are required for 'input' dialog type.")
    elif dialog_type == "confirm":
        if message:
            return yes_no_dialog(title="Confirmation", text=message).run()
        else:
            print("'message' is required for 'confirm' dialog type.")
    elif dialog_type == "checkbox":
        if message and choices:
            return checkboxlist_dialog(title="CheckboxList dialog", text=message, values=choices).run()
        else:
            print("'message' and 'choices' are required for 'checkbox' dialog type.")
    else:
        print("Invalid 'dialog_type'. Options: 'input', 'confirm', 'checkbox'.")

def _input_(message: str = None, input_type: Literal["pause", "confirm", "_input_", "hide", "choice"] = None, choices: List[str] = None) -> Union[None, bool, str]:
    """
    A function for handling user inputs in the terminal.

    Example:
        ```python
        import zyx
        zyx.input(message="Press Enter to continue...", input_type="pause")
        zyx.input(message="What is your name?", input_type="_input_")
        zyx.input(message="Are you sure?", input_type="confirm")
        zyx.input(message="Enter your password:", input_type="hide")
        zyx.input(message="Choose a color:", choices=["Red", "Green", "Blue"], input_type="choice")
        ```

    Args:
        message (str): The message to display to the user.
        input_type (str): Type of input to prompt for. Options: 'pause', 'confirm', '_input_', 'hide', 'choice'.
        choices (List[str]): A list of choices for the user to select from. Only required for 'choice' input_type.
    """
    if input_type == "pause":
        if not message:
            message = "Press Enter to continue..."
        input(message)
    elif input_type == "confirm":
        if not message:
            message = "Are you sure? (y/n): "
        else:
            message = f"{message} (y/n): "
        while True:
            value = input(message).lower()
            if value in ('y', 'yes'):
                return True
            elif value in ('n', 'no'):
                return False
            else:
                print("Invalid input. Please enter 'y' or 'n'.")
    elif input_type == "_input_":
        if message:
            return prompt(f"{message} ")
        else:
            print("'message' is required for '_input_' input type.")
    elif input_type == "hide":
        if message:
            return getpass(f"{message} ")
        else:
            print("'message' is required for 'hide' input type.")
    elif input_type == "choice":
        if message and choices:
            return prompt(message=f"{message} ", completer=WordCompleter(words=choices))
        else:
            print("'message' and 'choices' are required for 'choice' input type.")
    else:
        print("Invalid 'input_type'. Options: 'pause', 'confirm', '_input_', 'hide', 'choice'.")

# Example usage
if __name__ == "__main__":
    dialog(message="What is your name?", title="Input", dialog_type="input")
    dialog(message="Are you sure?", dialog_type="confirm")
    dialog(message="Choose colors:", choices=[("Red", True), ("Green", False), ("Blue", False)], dialog_type="checkbox")

    _input_(message="Press Enter to continue...", input_type="pause")
    _input_(message="What is your name?", input_type="_input_")
    _input_(message="Are you sure?", input_type="confirm")
    _input_(message="Enter your password:", input_type="hide")
    _input_(message="Choose a color:", choices=["Red", "Green", "Blue"], input_type="choice")