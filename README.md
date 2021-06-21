# cubejsclient

[![](https://img.shields.io/pypi/v/cubejsclient.svg)](https://pypi.org/pypi/cubejsclient/) [![License](https://img.shields.io/badge/License-BSD%203--Clause-blue.svg)](https://opensource.org/licenses/BSD-3-Clause)

Async Python Cube.js client

Features:

- Cube.js API client that makes async requests
- Rich objects for building queries with measures, dimensions, etc.

Table of Contents:

- [Installation](#installation)
- [Development](#development)

## Installation

cubejsclient requires Python 3.6 or above.

```bash
pip install cubejsclient
```

## Development

To develop cubejsclient, install dependencies and enable the pre-commit hook:

```bash
pip install pre-commit poetry
poetry install
pre-commit install
```

To run tests:

```bash
poetry shell
pytest
```
