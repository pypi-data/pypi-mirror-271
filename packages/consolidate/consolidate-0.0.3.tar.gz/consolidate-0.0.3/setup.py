"""A setuptools based setup module.

See:
https://packaging.python.org/guides/distributing-packages-using-setuptools/
https://github.com/pypa/sampleproject
"""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()

long_description = (here / "README.md").read_text(encoding="utf-8")

setup(
    name="consolidate",
    version="0.0.3",
    description="A Python library for generating a list of strings with every possible combination of placements of a given character (or a zero-width non joiner by default) within another given string, up to a given maximum length of characters.",
    long_description="Consolidate A Python library for generating a list of strings with every possible combination of placements of a given character (or a zero-width non joiner by default) within another given string, up to a given maximum length of characters.",
    long_description_content_type='text/markdown',
    url="https://github.com/ThePilot4571/consolidate-py/", 
    author="ThePilot4571",
    author_email="nocosecantoftheta@gmail.com",
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: Unix",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: MacOS :: MacOS X"
    ],
    keywords=['python', 'spaces','string','username','spam'],
    packages=find_packages(),
    install_requires=[],
    project_urls={
        "Source": "https://github.com/ThePilot4571/consolidate-py/",
    },
)