from setuptools import setup, find_packages

VERSION = "0.0.1"
DESCRIPTION = "My first package"
LONG_DESCRIPTION = "This is my first python package"

setup(
    name="lisa",
    version=VERSION,
    author="Suwilanji Jack Chipofya",
    author_email="suwilanjichipofya@outlook.com",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    keywords=["python", "stock data"],
    classifiers= [
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Education",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)