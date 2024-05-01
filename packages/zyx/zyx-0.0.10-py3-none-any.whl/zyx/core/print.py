from rich.console import Console
from rich.panel import Panel
from rich import box
from rich.columns import Columns
from typing import Optional, Literal, Any

# Define the Literal type for box styles
BoxStyle = Optional[Literal['SQUARE', 'ROUNDED', 'SIMPLE', 'DOUBLE', 'MINIMAL', 'HEAVY', 'ASCII']]

def _print_(*values: Any, _style_: Optional[str] = "white", _box_style_: BoxStyle = None, sep: str = ' ', end: str = '\n'):
    """
    Prints a message with the specified style and optionally in a box with the chosen style.

    Example:
        ```python
        from zyx import print

        print("This is a message with a box!", _box_style_="ROUNDED")
        print("This is a message without a box.")
        print("Multiple", "values", "printed", "with", "a", "separator", sep="-")
        print(1, 2, 3, 4, 5, sep=", ", end=" | ")
        ```

    Args:
        *values: The values to print.
        _style_ (str): The style to apply to the message.
        _box_style_ (BoxStyle): The style of the box to display the message in, or None to display without a box.
        sep (str): The separator between the values. Default is ' '.
        end (str): The string appended after the last value. Default is '\n'.

    Returns:
        Console: The Rich Console instance used for printing.
    """
    console = Console()

    if not values:
        values = ("No message provided.",)

    message = sep.join(str(value) for value in values)

    if isinstance(values, list):
        panels = [Panel(item, expand=False, box=getattr(box, _box_style_) if _box_style_ else None) for item in values]
        columns = Columns(panels)
        console.print(columns, style=_style_, end=end)
    else:
        if _box_style_:
            message = Panel(message, expand=False, box=getattr(box, _box_style_))
        console.print(message, style=_style_, end=end)

    return console

if __name__ == "__main__":
    _print_("[bold red]This is a message with a box![/bold red]", _box_style_="ROUNDED")
    _print_("This is a message without a box.")
    _print_("Multiple", "values", "printed", "with", "a", "separator", sep="-")
    _print_(1, 2, 3, 4, 5, sep=", ", end=" | ")