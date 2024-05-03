from setuptools import setup, find_packages

setup(
    author = "Hammad Saeed",
    author_email="hammad@supportvectors.com",

    name = 'zyx',
    version = '0.0.14',
    packages = find_packages(where='.zyx/src'),
    package_dir = {'': '.zyx/src'},

    python_requires = '>=3.8',

    package_data={
        '': ['vendor/*.whl'],  
    },

    install_requires = [
        # Art | ASCII Art
        'art',

        # IPython | Interactive Python
        'ipython',

        # LiteLLM | Easy LLM Completions
        'litellm',

        # Loguru | Logging
        'loguru',

        # Ollama | Language Models
        'ollama',

        # Pathlib | File Paths
        'pathlib',

        # Prompt Toolkit | Interactive Prompts
        'prompt_toolkit',

        # psutil | System Utilities
        'psutil',

        # Pydantic | Data Validation
        'pydantic',

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