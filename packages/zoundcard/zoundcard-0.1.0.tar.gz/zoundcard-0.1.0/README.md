# zoundcard

This library is using the
[pyaudio](https://people.csail.mit.edu/hubert/pyaudio/) and
[zignal](https://github.com/ronnyandersson/zignal) libraries to play audio on a
soundcard. This code was previously a part of the zignal library but split out
into its own.

## Pre-requisites

This library relies on pyaudio, which depends on the python development headers
and the portaudio development files. On debian/ubuntu,

    sudo apt install python3-dev portaudio19-dev

## Installation

It is recommended to create a virtual environment and let pip install the
dependencies automatically.

    python3 -m venv <name-of-virtualenv>
    . <name-of-virtualenv>/bin/activate
    pip install zoundcard

## Local development

Create a python3 virtualenv and install from the local source code to make the
library editable.

    python3 -m venv venv_dev
    . venv_dev/bin/activate
    pip install --editable .[dev]

### Style checks

Validate the imports

    isort src/**/*.py --check-only

Show suggested edits

    isort src/**/*.py --diff

Style guide enforcement using flake8

    flake8 --extend-ignore=E265 --statistics src/

### Unit tests

    python -m unittest -v src/tests/test_*.py

## Build a release

    python3 -m venv venv_build
    . ./venv_build/bin/activate
    pip install --upgrade pip build twine
    python3 -m build

### Upload packages

Upload to pypi.org using twine

    twine upload dist/*
