# PyO3

[PyO3](https://github.com/pyo3/pyo3) provides [Rust](https://www.rust-lang.org/) bindings for Python. In [this example](../../experiment/pyo3-helloworld/):

- [src/lib.rs](../../experiment/pyo3-helloworld/src/lib.rs) provides a function which returns a string
- [python/caller.py](../../experiment/pyo3-helloworld/python/caller.py) calls the function and prints the string.

## How to build

[`maturin`](https://github.com/PyO3/maturin) is used in [pyproject.toml](../../experiment/pyo3-helloworld/pyproject.toml). To build and run the project, run the following commands inside the subproject folder:

```bash
source .venv/bin/activate
maturin develop
python python/caller.py
```

> **NOTE**: For this local extension experiment, avoid running `maturin` through `uv run`. In testing, uv reused cached editable build artifacts, so changes to the Rust source did not always appear in the installed Python module. Activating the project virtual environment and running `maturin develop` directly made the rebuild/install loop easier to reason about.

## Type stub generation (`*.pyi` files)

In [PEP 484](https://peps.python.org/pep-0484/) it says:

> Stub files are files containing type hints that are only for use by the type checker, not at runtime.

Without a stub file, the language server doesn't know what are provided from the Rust implementation. PyO3 has a work-in-progress experimental feature [`experimental-inspect`](https://pyo3.rs/main/features.html#experimental-inspect). The progress can be tracked from [PyO3/pyo3#5137](https://github.com/PyO3/pyo3/issues/5137). After enabling it in `Cargo.toml`:

```toml
[dependencies]
pyo3 = { version = "0.29.0", features = ["experimental-inspect"] }
```

Calling `maturing develop --generate-stubs` will generate `*.pyi` files as well.

## Type conventions

In [this page](https://pyo3.rs/main/conversions/tables.html) there are two table:

- Argument Types: the Python types that will be converted to function argument types
- Returning Rust values to Python

## Related Topics and Links

- [Foreign Function Interface](../concepts/ffi.md)
- [PyO3 User Guide](https://pyo3.rs/)
- [PyO3 API](https://docs.rs/pyo3/)
