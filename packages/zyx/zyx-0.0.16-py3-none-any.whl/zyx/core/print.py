from rich.console import Console
from rich.panel import Panel
from rich import box
from rich.columns import Columns
from typing import Optional, Literal, Any

# Define the Literal type for box styles
BoxStyle = Optional[Literal['SQUARE', 'ROUNDED', 'SIMPLE', 'DOUBLE', 'MINIMAL', 'HEAVY', 'ASCII']]

class RichPrint:
    def __init__(self):
        self.console = Console()

    def print(self, *values: Any, style: Optional[str] = "white", box_style: BoxStyle = None, sep: str = ' ', end: str = '\n'):
        """
        Prints a message with the specified style and optionally in a box with the chosen style.

        Example:
        ```python
        from zyx import print
        print("This is a message with a box!", box_style="ROUNDED")
        print("This is a message without a box.")
        print("Multiple", "values", "printed", "with", "a", "separator", sep="-")
        print(1, 2, 3, 4, 5, sep=", ", end=" | ")
        ```

        Args:
            *values: The values to print.
            style (str): The style to apply to the message.
            box_style (BoxStyle): The style of the box to display the message in, or None to display without a box.
            sep (str): The separator between the values. Default is ' '.
            end (str): The string appended after the last value. Default is '\n'.

        Returns:
            None
        """
        if not values:
            values = ("No message provided.",)
        message = sep.join(str(value) for value in values)

        if isinstance(values, list):
            panels = [Panel(item, expand=False, box=getattr(box, box_style) if box_style else None) for item in values]
            columns = Columns(panels)
            self.console.print(columns, style=style, end=end)
        else:
            if box_style:
                message = Panel(message, expand=False, box=getattr(box, box_style))
            self.console.print(message, style=style, end=end)

_print_ = RichPrint().print