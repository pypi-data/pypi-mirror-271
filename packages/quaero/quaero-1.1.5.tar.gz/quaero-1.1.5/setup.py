from setuptools import setup, find_packages
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="quaero",
    version="1.1.5",
    description="Simple CLI tool for asking ChatGPT questions in the CLI",
    long_description=long_description,
    long_description_content_type='text/markdown',
    author="Gillian Yeomans",
    author_email="hello@gillian.codes",
    url="https://github.com/yeo-yeo/chatgpt-cli-python",
    packages=find_packages(),
    install_requires=["aiohttp", "colorama", "python-dotenv"],
    entry_points={
        "console_scripts": [
            "quaero=quaero.index:main",
        ],
    },
)
