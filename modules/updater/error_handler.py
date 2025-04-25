import functools
import inspect
import os


def fancy_error_handler(func):
    """Decorator that wraps function in try-except and handles errors with file info and Streamlit support."""

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            # Get function name and file info for better error messages
            func_name = func.__name__
            file_path = inspect.getfile(func)
            file_name = os.path.basename(file_path)

            error_message = f"""{file_name}.{func_name}:\nError message:\n
    {e}\nDisable @fancy_error_handler to see the full traceback."""
            print(error_message)
            # Sprawdź, czy pierwszy argument jest obiektem Streamlit
            if args and hasattr(args[0], "error") and callable(args[0].error):
                args[0].error(error_message)

            return False

    return wrapper


def scraping_error_handler(func):
    """Decorator for scraping methods that handles errors gracefully."""

    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        try:
            result = func(self, *args, **kwargs)
            # Return None for empty result
            return result if result is not None else None
        except Exception as e:
            class_name = self.__class__.__name__
            func_name = func.__name__
            print(f"""Fetching error:   {class_name:<14} ->   {func_name:<14}    {e}""")
            return None

    return wrapper


def no_offers_found(website, link):
    """Check if the website has no offers."""
    message = f"No offers found for {website}: {link}"
    print(message)
    return ""
