from rich.console import Console
from rich.status import Status
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeElapsedColumn
from rich.panel import Panel
from rich import box
import time
import contextlib

# ==============================================================================

@contextlib.contextmanager
def show_loader(message="Loading...", spinner="dots", use_box=False):
    """Displays an animated loading status using the Rich library."""
    console = Console()
    if use_box:
        status = Status(Panel(message, expand=False, box=box.ROUNDED), spinner=spinner, console=console)
    else:
        status = Status(message, spinner=spinner, console=console)
    status.start()
    try:
        yield status
    finally:
        status.stop()

def update_loader(status, message):
    """Updates the loading message."""
    if isinstance(status.renderable, Panel):
        status.update(Panel(message, expand=False, box=box.ROUNDED))
    else:
        status.update(message)

# Usage example
if __name__ == "__main__":
    with show_loader(message="Processing data", spinner="dots") as loader:
        time.sleep(2)
        update_loader(loader, "Processing step 1")
        time.sleep(2)
        update_loader(loader, "Processing step 2")
        time.sleep(2)

# ==============================================================================
@contextlib.contextmanager
def show_progress(total: int):
    """Displays a progress bar using the Rich library."""
    if not total:
        raise ValueError("The 'total' argument is required.")
    console = Console()
    columns = [
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        TimeElapsedColumn()
    ]
    progress = Progress(*columns, console=console)
    task = progress.add_task("[cyan]Processing...", total=total)
    progress.start()
    try:
        yield progress, task
    finally:
        progress.stop()

def update_progress(progress, task, completed: int):
    """Updates the progress bar with the number of completed steps."""
    progress.update(task, advance=completed)

# Usage example
if __name__ == "__main__":
    with show_progress(total=100) as (progress, task):
        for i in range(100):
            update_progress(progress, task, 1)
            time.sleep(0.1)