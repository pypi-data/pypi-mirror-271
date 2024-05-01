"""
Setup configuration for compsio core.
"""

import os
from pathlib import Path
from setuptools import setup
from setuptools import setup, find_packages

setup(
    name="composio_core",
    version="0.2.39",
    author="Utkarsh",
    author_email="utkarsh@composio.dev",
    description="Core package to act as a bridge between composio platform and other services.",
    long_description=(Path(__file__).parent / "README.md").read_text(encoding="utf-8"),
    long_description_content_type="text/markdown",
    url="https://github.com/SamparkAI/composio_sdk",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9,<4",
    packages=find_packages(include=["composio*"]),
    entry_points={
        "console_scripts": [
            "composio-cli=composio.composio_cli:main",
        ],
    },
    install_requires=[
        "requests>=2.31.0,<3",
        "jsonschema>=4.21.1,<5",
        "beaupy>=3.7.2,<4",
        "termcolor>=2.4.0,<3",
        "pydantic>=2.6.4,<3",
        "openai>=1.3.0",
        "rich>=13.7.1,<14",
        "importlib-metadata>=4.8.1,<5",
        "pyperclip>=1.8.2,<2",
    ],
    include_package_data=True,
)
