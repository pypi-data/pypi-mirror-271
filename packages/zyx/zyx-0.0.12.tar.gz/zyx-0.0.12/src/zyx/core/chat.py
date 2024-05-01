import ollama
import json
from typing import Literal, Optional

def chat(prompt: str = None, model: Optional[str] = 'llama3'):
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