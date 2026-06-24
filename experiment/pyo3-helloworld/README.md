# PyO3 Helloworld

This is an experiment project to get familiar how to wire up implementations in Rust to Python.

In this example:

- [src/lib.rs](./src/lib.rs) provides a function which returns a string
- [python/caller.py](./python/caller.py) calls the function and prints the string.

## How to build

[`maturin`](https://github.com/PyO3/maturin) is used in [pyproject.toml](./pyproject.toml). To build and run the project, run the following commands inside the subproject folder:

```bash
source .venv/bin/activate
maturin develop --generate-stubs
python python/caller.py
```

> **NOTE**: For this local extension experiment, avoid running `maturin` through `uv run`. In testing, uv reused cached editable build artifacts, so changes to the Rust source did not always appear in the installed Python module. Activating the project virtual environment and running `maturin develop` directly made the rebuild/install loop easier to reason about.
