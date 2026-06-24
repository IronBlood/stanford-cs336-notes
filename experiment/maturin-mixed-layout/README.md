# Experiment: mixed layout of Python / Rust using maturin

In the [previous experiment](../pyo3-helloworld/), the Rust part acts more like a complete Python package, while the [test script](../pyo3-helloworld/python/caller.py) works as an individual script which doesn't belong to any package. `maturin develop` will install the package to the virtual environment and the test script can load the package correctly.

However this flow doesn't work for a project managed by `uv`, because `uv` checks the installed dependencies. A local developed package isn't registered in `pyproject.toml`, so it will be removed once `uv run` is executed.

This project follows [the document of project layout](https://www.maturin.rs/project_layout.html) to use a mixed approach.

The library name in `Cargo.toml`, `lib.rs` has to match the Python package name. In this project, it is set to `my_project`. When `maturin develop` is called, the native extension (a `.so` file under Linux) is installed to `my_project/` instead of the virtual env. `--generate-stubs` also works in this case, it generates `my_project/my_project.pyi`.

`uv run my_project/bar.py` fails, it complains that "ImportError: attempted relative import with no known parent package".

Instead `uv run python -m my_project.bar` is the correct way. Since the native extension lives now under the source folder, `uv` will not delete it.

`uv` may invoke `maturin` during the call, thus regenerate the native extension. But this does not always happen. The stub file isn't generated if `uv` invokes `maturin`. There might be some configurations for `[tool.maturin]` but haven't found yet.

So in short, the best workflow:

1. run `maturin` manually (first activate the virtual environment, then `maturin develop --generate-stubs`).
2. call `uv run` as usual
