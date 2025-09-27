#!/usr/bin/env python3
"""
Setup script for Photo Converter
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read the contents of README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding='utf-8')

setup(
    name="photo-converter",
    version="1.0.0",
    author="Photo Converter Project",
    author_email="",
    description="A user-friendly Python application for converting images between different formats with special support for iPhone HEIC photos",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/acidbathbob/photo-converter",
    packages=find_packages(),
    package_dir={"": "src"},
    py_modules=["photo_converter", "photo_converter_gui"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Multimedia :: Graphics :: Graphics Conversion",
        "Topic :: Utilities",
    ],
    python_requires=">=3.8",
    install_requires=[
        "Pillow>=10.0.0",
        "click>=8.0.0",
        "tqdm>=4.65.0",
        "pillow-heif>=1.1.0",
    ],
    extras_require={
        "dev": [
            "pytest>=6.0",
            "black>=22.0",
            "flake8>=4.0",
        ]
    },
    entry_points={
        "console_scripts": [
            "photo-converter=photo_converter:main",
            "photo-converter-gui=launch_gui:main",
        ],
    },
    scripts=[
        "launch_gui.py",
    ],
    include_package_data=True,
    keywords="image converter heic jpeg png webp gui batch photo iphone",
    project_urls={
        "Bug Reports": "https://github.com/acidbathbob/photo-converter/issues",
        "Source": "https://github.com/acidbathbob/photo-converter",
        "Documentation": "https://github.com/acidbathbob/photo-converter#readme",
    },
)