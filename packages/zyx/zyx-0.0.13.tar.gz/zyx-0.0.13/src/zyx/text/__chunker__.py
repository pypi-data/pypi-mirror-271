import semchunk
import tiktoken
from typing import Optional

def chunk_text(text : str = None, chunk_size : Optional[int] = 100) -> list[str]:
    """
    A Function that utilizes the semchunk library to chunk text into smaller pieces

    Example:
        ```python
        from zyx.functions.chunk_text import chunk_text

        text = "This is a sample text that we want to chunk into smaller pieces"
        chunked_text = chunk_text(text = text, chunk_size = 100)
        print(chunked_text)
        ```

    Args:
        text (str): The text that you want to chunk
        chunk_size (int): The size of the chunks that you want to split the text into

    Returns:
        list[str]: A list of strings that are the chunks of the text
    """
    if not text:
        raise ValueError("No text provided")
    encoder = tiktoken.encoding_for_model('gpt-4')
    token_counter = lambda text: len(encoder.encode(text))
    try:
        chunked_text = semchunk.chunk(
                    text = text,
                    chunk_size = chunk_size,
                    token_counter = token_counter)
        return chunked_text
    except Exception as e:
        print(f"Error: {e}")
        return None
