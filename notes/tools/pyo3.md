# PyO3

[PyO3](https://github.com/pyo3/pyo3) provides [Rust](https://www.rust-lang.org/) bindings for Python.

There are two related experiments:

- [pyo3-helloworld](../../experiment/pyo3-helloworld): the first experiment tries to explore how to wire up Rust and Python.
- [maturin-mixed-layout](../../experiment/maturin-mixed-layout/): the second experiment tries to pair `maturin` together with `uv`

## Type stub generation (`*.pyi` files)

In [PEP 484](https://peps.python.org/pep-0484/) it says:

> Stub files are files containing type hints that are only for use by the type checker, not at runtime.

Without a stub file, the language server doesn't know what are provided from the Rust implementation. PyO3 has a work-in-progress experimental feature [`experimental-inspect`](https://pyo3.rs/main/features.html#experimental-inspect). The progress can be tracked from [PyO3/pyo3#5137](https://github.com/PyO3/pyo3/issues/5137). After enabling it in `Cargo.toml`:

```toml
[dependencies]
pyo3 = { version = "0.29.0", features = ["experimental-inspect"] }
```

Calling `maturin develop --generate-stubs` will generate `*.pyi` files as well.

## Type conventions

In [this page](https://pyo3.rs/main/conversions/tables.html) there are two tables:

- Argument Types: the Python types that will be converted to function argument types
- Returning Rust values to Python

## Related Topics and Links

- [Foreign Function Interface](../concepts/ffi.md)
- [PyO3 User Guide](https://pyo3.rs/)
- [PyO3 API](https://docs.rs/pyo3/)
