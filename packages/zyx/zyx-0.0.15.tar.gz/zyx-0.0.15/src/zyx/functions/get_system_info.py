import psutil
from typing import Optional, Tuple

def system_info(verbose : Optional[bool] = False) -> list[Tuple[str, float]]:
    """
    A function to get system information such as CPU cores, CPU usage, memory, and swap memory.

    Example:
        ```python
        import zyx

        zyx.system_info(verbose=True)
        ```

    Args:
        verbose (bool, optional): Whether to print the system information. Defaults to False.

    Returns:
        list[Tuple[str, float]]: A list of tuples containing the system information.
    """
    cpu_count = psutil.cpu_count(logical=True)
    usable_cpu_count = psutil.cpu_count(logical=False)
    cpu_usage = psutil.cpu_percent(interval=1)

    total_memory = psutil.virtual_memory().total / (1024 ** 3)  # Convert bytes to GB
    available_memory = psutil.virtual_memory().available / (1024 ** 3)  # Convert bytes to GB
    total_swap = psutil.swap_memory().total / (1024 ** 3)
    free_swap = psutil.swap_memory().free / (1024 ** 3)

    info = [
        ('Total CPU Cores', cpu_count),
        ('Usable CPU Cores', usable_cpu_count),
        ('CPU Usage (%)', cpu_usage),
        ('Total Memory (GB)', round(total_memory, 2)),
        ('Available Memory (GB)', round(available_memory, 2)),
        ('Total Swap Memory (GB)', round(total_swap, 2)),
        ('Free Swap Memory (GB)', round(free_swap, 2))
    ]

    if verbose:
        for label, value in info:
            print(f'{label}: {value}')

    return info
