# Flit backed packaging tool

Python package (i.e., wheel or sdist).

It relies on Flit as a build backend with pyproject.toml for configuration.

flit (like setuptools) doesn't manage your virtual environment.

## Editable install:

    flit install --symlink --deps=all

## Run code:
    python -c "import flit_demo_package"

## Build:

    flit build

## Upload to PyPI:
    flit publish
