from setuptools import setup, find_packages
from pathlib import Path

this_directory = Path(__file__).parent

VERSION = "1.0.0"
DESCRIPTION = "A private database service library."
LONG_DESCRIPTION = (this_directory / "README.md").read_text()

# Setting up
setup(
    name="pydbconnect",
    version=VERSION,
    author="NexusNovelist",
    author_email="<proffesionalnoice@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=["requests"],
    keywords=["python", "database", "server"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ],
)
