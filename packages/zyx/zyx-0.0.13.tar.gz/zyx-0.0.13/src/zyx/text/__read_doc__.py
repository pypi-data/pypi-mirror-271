import fitz

def read_file(file_path: str) -> str:
    """
    A simple function using fitz to read the contents of a file. Including PDFs

    Example:
        ```python
        import zyx

        content = zyx.read_file("example.txt")
        print(content)
        ```

    Args:
        file_path (str): The path to the file to read.

    Returns:
        str: The content of the file.    
    """
    if not file_path:
        return "No file path provided."

    if file_path.endswith(".pdf"):
        with fitz.open(file_path) as doc:
            content = " ".join(page.get_text() for page in doc)
    else:
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()
    return content