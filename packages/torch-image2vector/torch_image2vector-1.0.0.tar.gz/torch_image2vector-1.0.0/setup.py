#!/usr/bin/env python
"""Setup for torch_image2vector"""

import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="torch_image2vector",
    version="1.0.0",
    author="lukasz-majewski",
    description="Extract images embeddings with variation of pre-trained torch models",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/MajewskiLukasz/torch_image2vector",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=[
        "torch",
        "torchvision",
        "numpy>=1.23.0",
        "Pillow>=9.1.1",
    ],
)
