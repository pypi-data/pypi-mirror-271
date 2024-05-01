import pathlib

def validate_dir_exists(path: str) -> str:
    """
    A function to validate if a directory exists.

    Example:
        ```python
        import zyx

        path = zyx.validate_dir_exists("/path/to/directory")
        ```

    Args:
        path (str): The path to the directory.

    Returns:
        str: The path to the directory.
    """
    if not path:
        raise ValueError("Path is required!")
    try:
        path = pathlib.Path(path)
        if not path.exists():
            raise FileNotFoundError(f"Directory not found: {path}")
        if not path.is_dir():
            raise ValueError(f"Path is not a directory: {path}")
    except Exception as e:
        raise ValueError(f"Error reading path: {e}")

    return str(path)


def validate_file_exists(path: str) -> str:
    """
    A function to validate if a file exists.

    Example:
        ```python
        import zyx

        path = zyx.validate_file_exists("/path/to/file")
        ```
    
    Args:
        path (str): The path to the file.

    Returns:
        str: The path to the file.
    """
    if not path:
        raise ValueError("Path is required!")

    try:
        path = pathlib.Path(path)
        if not path.exists():
            raise FileNotFoundError(f"File not found: {path}")
        if not path.is_file():
            raise ValueError(f"Path is not a file: {path}")
    except Exception as e:
        raise ValueError(f"Error reading: {e}")

    return str(path)


def create_path(path: str) -> str:
    """
    A function to create a directory if it does not exist. 

    Example:
        ```python
        import zyx

        path = zyx.create_path("/path/to/directory")
        ```

    Args:
        path (str): The path to the directory.
    """
    if not path:
        raise ValueError("Path is required!")
    try:
        path = pathlib.Path(path)
        path.mkdir(parents=True, exist_ok=True)
    except Exception as e:
        raise ValueError(f"Error creating path: {e}")

    return str(path)


def validate_file_extension(file_path: str, valid_extensions: list) -> str:
    """
    A function to validate if a file has a valid extension.

    Example:
        ```python
        import zyx

        path = zyx.validate_file_extension("/path/to/file.txt", valid_extensions=[".txt"])
        ```

    Args:
        file_path (str): The path to the file.
        valid_extensions (list): A list of valid extensions.
    """
    if not file_path:
        raise ValueError("File path is required!")

    if not valid_extensions:
        raise ValueError("Valid extensions are required!")

    file_extension = pathlib.Path(file_path).suffix.lower()
    if file_extension not in valid_extensions:
        raise ValueError(f"Invalid file extension: {file_extension}. Valid extensions: {valid_extensions}")

    return file_path


def validate_not_empty(value: str, field_name: str) -> str:
    """
    A function to validate if a value is not empty.

    Example:
        ```python
        import zyx

        value = zyx.validate_not_empty("Hello World!", field_name="Message")
        ```

    Args:
        value (str): The value to validate.
        field_name (str): The name of the field.

    Returns:
        str: The value.
    """
    if not value:
        raise ValueError(f"{field_name} cannot be empty!")

    return value

if __name__ == "__main__":
    val = validate_dir_exists("/home/hammad/Development/yosemite/src/yosemite/functions/gadgets")
    print(val)