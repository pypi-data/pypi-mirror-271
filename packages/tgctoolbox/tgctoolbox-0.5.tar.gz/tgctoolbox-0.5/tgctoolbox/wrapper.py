import functools
import time
import warnings

from colorama import Fore
from colorama import Style

from .timing import log_time


def custom_formatwarning(msg, *args, **kwargs):
    """
    Customize the format of warning messages.

    This function alters the default warning format to include color coding using colorama.
    It is set as the default format for warnings throughout the project.

    Args:
        msg: The warning message to format.
        *args: Additional arguments.
        **kwargs: Additional keyword arguments.

    Returns:
        str: The formatted warning message.
    """
    return f"{Fore.YELLOW}WARNING: {Style.RESET_ALL}{str(msg)}\n"


warnings.formatwarning = custom_formatwarning


def experimental_feature(func):
    """
    A decorator to mark a function as experimental.

    This decorator wraps a function and issues a warning when the function is called,
    indicating that it is an experimental feature. This is useful for alerting users of
    potentially unstable or changing features.

    Args:
        func (Callable): The function to be decorated.

    Returns:
        Callable: The wrapped function with a warning on call.
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        """
        Wrapper function to display a warning when the decorated function is called.

        Args:
            *args: Arguments passed to the function.
            **kwargs: Keyword arguments passed to the function.

        Returns:
            The result of the wrapped function call.
        """
        warnings.warn(
            f"[{func.__name__}] This is an experimental feature and may change in the future.",
            UserWarning,
        )
        return func(*args, **kwargs)

    return wrapper


def timeit(func):
    """
    A decorator to measure the execution time of a function.

    This decorator wraps a function and measures the time it takes to execute.
    The duration is logged using the TGCLogger class.

    Args:
        func (Callable): The function to be decorated.

    Returns:
        Callable: The wrapped function with timing information.
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        """
        Wrapper function to measure the execution time of the decorated function.

        Args:
            *args: Arguments passed to the function.
            **kwargs: Keyword arguments passed to the function.

        Returns:
            The result of the wrapped function call.
        """
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        log_time(start_time, end_time, f"Execution time for {func.__name__}")
        return result

    return wrapper
