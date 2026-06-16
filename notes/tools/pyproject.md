# pyproject.toml

This file acts as a package configuration file. It's written in [TOML](https://toml.io/en/), and may contain sections such as `build-system`, `project` and `tool.*`:

```toml
# https://packaging.python.org/en/latest/specifications/pyproject-toml/#pyproject-project-table
[project]
name = "my-package"
version = "0.1.0"
dependencies = []
requires-python = ">=3.12"

# https://packaging.python.org/en/latest/specifications/pyproject-toml/#pyproject-build-system-table
[build-system]
requires = ["setuptools"]

# https://packaging.python.org/en/latest/specifications/pyproject-toml/#pyproject-tool-table
[tool.pyright]
venvPath = "."
venv = ".venv"
```

It is the modern standard for Python projects. Its major standardized parts are defined by [PEP 518](https://peps.python.org/pep-0518/) and [PEP 621](https://peps.python.org/pep-0621/). It replaces many older uses of `setup.py` and `setup.cfg`. It can also replace simple `requirements.txt` files for project dependencies, though `requirements.txt` is still common for pinned environments.
