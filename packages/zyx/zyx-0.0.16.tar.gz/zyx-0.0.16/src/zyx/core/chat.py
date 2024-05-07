import ollama
import json
from typing import Literal, Optional

def chat(prompt: str = None, model: Optional[str] = 'llama3') -> str:
    """
    A simple function to use Ollama completions.

    Example:
        ```python
        import zyx
        zyx.chat("What is the meaning of life?")
        ```

    Parameters:
        - prompt: The text to send to the model.
        - model: The model to use. Default is 'llama3'.

    Returns:
        - The response from the model.
    """
    if not prompt:
        raise ValueError("No prompt provided")
    if not model:
        model = 'llama3'
    try:
        response = ollama.chat(
            model=model,
            messages=[{'role': 'user', 'content': prompt}],
        )
        return response['message']['content'].replace('\\n', '\n')
    except Exception as e:
        print(f"Error: {e}")
        return None