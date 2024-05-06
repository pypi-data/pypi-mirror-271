from setuptools import setup

# read the contents of your README file
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(name = "drop_needle",
      version = "0.2",
      description = "Simulate probability of a needle crossing a line on a table after it fell on it",
      long_description=long_description,
      long_description_content_type='text/markdown',
      packages = ["drop_needle"],
      author = "Martin Draws",
      zip_safe = False)