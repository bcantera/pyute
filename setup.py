import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="pyute",
    version="1.0.0",
    description="Python library to interact with UTE API services",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/bcantera/pyute",
    author="Braihan Cantera",
    author_email="",
    classifiers=(
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
    ),
    include_package_data=True,
    install_requires=["aiohttp"]
)
