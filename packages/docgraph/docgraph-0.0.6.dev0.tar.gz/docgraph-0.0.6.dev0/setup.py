import os, sys
import shutil
import yaml
from setuptools import setup, find_packages
from docgraph.version import config, VersionString

version_str = VersionString(config)

from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

# Setting up
setup(
    # the name must match the folder name 'docgraph'
    name="docgraph", 
    version=version_str,
    author="Brad Larson",
    author_email="<bhlarson@gmail.com>",
    description=config['description'],
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages(exclude="tests"),
    install_requires=['pyyaml', 'tqdm', 'pymupdf', 'tiktoken'], # add any additional packages that 
    url = 'https://ha-us.dso.thermofisher.net/artifactory/sci-ai-pypi-internal/docgraph',
    keywords=['python', 'Machine Learning', 'Document Graph'],
    include_package_data=True,
    package_data = {'docgraph': ['*.yaml']},
    classifiers= [
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3",
        "Operating System :: POSIX :: Linux",
    ]
)