# Docgraph Python Library

## Table of Contents
- [Constants](#constants)
- [Functions](#functions)
- [Classes](#classes)

## Setup

References:
- [Packaging Python Projects](https://www.freecodecamp.org/news/build-your-first-python-package/)
- [How to Publish an Open-Source Python Package to PyPI](https://realpython.com/pypi-publish-python-package/)
- [Set Up PyPI Repositories on Artifactory](https://jfrog.com/help/r/jfrog-artifactory-documentation/set-up-pypi-repositories-on-artifactory)
- [Publish PyPI Packages to Artifactory](https://jfrog.com/help/r/jfrog-artifactory-documentation/publish-pypi-packages-to-artifactory)

- Install twine:
    ```cmd
    pip3 install twine
    ```
- The [deploy](./deploy) script automates building and uploading the python packages
- Build whl:
    ```cmd
    py setup.py sdist bdist_wheel
    ```

- Upload package to pipy
    ```cmd
    twine upload dist/*

## Constants

## Functions

## Classes