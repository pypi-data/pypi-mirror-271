import sys
from typing import Any, Callable, Dict, Optional
from rich import rprint

# Set the default value for PRINT_ENABLED
PRINT_ENABLED = True

def get_var_name(var: Any) -> Optional[str]:
    """Get the name of a variable."""
    for name, val in globals().items():
        if val is var:
            return name
    return None

def get_human_readable_size(num_bytes: int) -> str:
    """Convert the number of bytes to a human-readable string."""
    units = ['B', 'KB', 'MB', 'GB', 'TB', 'PB']
    unit_index = 0
    size = num_bytes

    while size >= 1024 and unit_index < len(units) - 1:
        size /= 1024
        unit_index += 1

    return f"{size:.2f} {units[unit_index]}"


def get_var_size(x):
    return get_human_readable_size(sys.getsizeof(x))

    
def printt(x: Any, print_variable: bool = True) -> None:
    """Prints details about a variable."""
    global PRINT_ENABLED  # Declare the global variable within the function

    if not PRINT_ENABLED:
        return  # Exit the function early if printing is disabled

    just_print: Dict[str, Any] = {
        "name": get_var_name(x),
        "variable": x if print_variable else "print variable is disabled",
        "class": x.__class__.__name__,
    }

    rprint("-" * 60)
    for key, value in just_print.items():
        rprint(f"[bold blue]{key:15} ::[/bold blue] {value}")
    rprint("-" * 60)

    use_try: Dict[str, Callable] = {
        "type": type,
        "dir": dir,
        "len": len,
        "Memory Usage": get_var_size
    }

    for key, func in use_try.items():
        try:
            rprint(f"[bold magenta]{key:15} ::[/bold magenta] {func(x)}")
            rprint("-" * 60)
        except Exception as e:
            rprint(f"[bold red]{key:15} ::[/bold red] not printed due to {e} !!!")
            rprint("-" * 60)

    rprint()

def enable_printt():
    global PRINT_ENABLED
    PRINT_ENABLED = True

def disable_printt():
    global PRINT_ENABLED
    PRINT_ENABLED = False