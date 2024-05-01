from setuptools import setup, find_packages

setup(
    author = "Hammad Saeed",
    author_email="hammad@supportvectors.com",

    name = 'zyx',
    version = '0.0.10',
    packages = find_packages(where='src'),
    package_dir = {'': 'src'},

    python_requires = '>=3.8',

    install_requires = [
        # General Utility Libraries
        'art',
        'pathlib',
        'prompt_toolkit',
        'pydantic',
        'psutil',

        # LiteLLM | Easy LLM Completions
        'litellm',

        # Loguru | Logging
        'loguru',

        # Ollama | Language Models
        'ollama',

        # PyMuPDF4 | PDF Parsing
        'PyMuPDF',

        # Rich | Pretty Printing
        'rich',

        # SemChunk | Semantic Chunking
        'semchunk',

        # TikToken | Tokenization
        'tiktoken',
],
    entry_points={
        'console_scripts': [
            'zyx=zyx.__cli__:main',
        ]
    })