# Core Library modules
from typing import Any, Callable


def file_exception(func: Callable) -> Callable:
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        try:
            result = func(*args, **kwargs)
        except FileNotFoundError as e:  # pragma: no cover
            raise SystemExit("The file does not exist")
        except PermissionError as e:  # pragma: no cover
            raise SystemExit("Permission denied to file")
        except IsADirectoryError as e:  # pragma: no cover
            raise SystemExit("File is a directory not a file")
        except OSError as e:  # pragma: no cover
            raise SystemExit("A general IO error has occurred opening file")
        except UnicodeDecodeError:  # pragma: no cover
            raise SystemExit("Error decoding file. It may not be a valid text file.")
        except Exception as e:  # pragma: no cover
            raise SystemExit("An error occurred")
        return result

    return wrapper
