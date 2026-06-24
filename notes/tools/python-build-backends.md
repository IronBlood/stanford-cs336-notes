# Python Build Backends

A build backend transforms a source tree (i.e., a directory) into a source distribution or a wheel.

## A brief history of the Python packaging mechanisms

[Distutils](https://wiki.python.org/moin/Distutils) was a mechanism to distribute Python packages and extensions since [Python 1.6](https://www.python.org/download/releases/1.6/). It was part of the standard library, and was deprecated since version 3.10, removed in version 3.12.

Before it, packaging was extremely ad-hoc: projects shipped custom `Makefile`s, shell scripts, or OS-specific install instructions. `distutils` standardized the idea of a `setup.py` and a declarative-ish metadata + build process.

> NOTE: the final version of Python 1.6 was released on September 5, 2000. `distutils` was never a "backend" in the modern sense of PEP 517/518. It was both a build system, an installer and part of the standard library.

`setuptools` appeared around 2004. It was introduced as a layer built on top of `distutils` to fix practical ecosystem pain points that were already emerging:

1. Dependency management: `distutils` could describe a package, but not reliably express or install dependencies from other packages.
2. Reproducible installation workflows: `setuptools` introduced mechanisms like "fetch dependencies during install".
3. Package discovery / namespace handling: it introduced `find_packages()`
4. Entry points: this became a key feature: declaring "this  package provides a command-line tool" or plugin hooks, and later became foundational for plugin ecosystems (pytest, sphinx, etc.).
5. Better support for binary extensions: it extended `distutils`' ability to compile C/C++ extensions in a more flexible way.

`easy_install` was part of `setuptools`. Its main goal was simple and very ambitious for the time: install Python packages automatically from the internet, including their dependencies. Before it, installing anything usually meant downloading a tarball,  running `setup.py install` and manually resolving missing dependencies. `easy_install` tried to automate that entire flow.

> NOTE: `easy_install` also had its weakness, however this page is more about building and packaging, we are not going to talk about the details.

Around 2008 `pip` was created to fix problems in `easy_install`. For a few years both coexisted: `easy_install` still came bundled with `setuptools`, `pip` was initially optional and not always installed by default. Over time, `pip` became the default recommendation in documentation, tutorials, and OS packaging. By Python 3.x era (especially Python 3.4+), `pip` was effectively the standard tool, and Python even started shipping `pip` by default.

## PEP 517 (and 518)

In [pyproject](./pyproject.md) we have already mentioned PEP 518. Before [PEP 517](https://peps.python.org/pep-0517/), tools like `pip` worked like this:

1. Download source distribution.
2. Run `setup.py install` (or similar entry point)
3. Let the project's own Python code decide how to build/install itself

This flow created a deep coupling:

* The build logic was arbitrary Python code (`setup.py`)
* The installer (`pip`) had to *execute user code to install packages*
* There was no standard way to ask: "How do I build this project?"

There was no clean abstraction layer between "install tool" and "build system".

**PEP 517** formalized a separation:

> A build frontend MAY use any mechanism for setting up a build environment that meets the above criteria.

Instead of running `setup.py`, pip now asks:

* "Give me a wheel"
* "What are your build requirements?"

via a standardized API exposed by a backend.

So before PEP 517, it was like "every project is a Python script that builds itself", and after PEP 517, "every project declares a build system that implements a standard interface".

So packaging was split into two roles:

* **Frontend**: pip (installs things)
* **Backend**: build source distributions and wheels.

PEP 517 didn't introduce new build tools, it only introduced a contract:

* allow projects to declare build system in `pyproject.toml`
* allow multiple build systems (not just setuptools)
* let pip stop executing arbitrary project code directly
* standardized wheel building

## Backend options

There are many options:

### `setuptools`

It's legacy but still dominant, still the most widely used backend. It's extremely compatible, supports almost everything (C extensions, legacy patterns). But the configuration might be complex, and it inherited a lot of legacy behavior.

### `hatch` (frontend) / `hatchling` (backend)

It's modern, `pyproject.toml`-first design, good for pure-Python projects.

### `flit`

One of the earliest "PEP 517-native" tools, focus on pure Python packages only, extremely minimal and predictable.

### `maturin`

Already introduced in [PyO3](./pyo3.md). It's a backend specialized for Rust-based Python extensions, not a general-purpose pure-Python backend.

### `uv` (frontend) / `uv_build` (backend)

This is slightly different conceptually.

`uv` is primarily:

* installer
* resolver
* environment manager

like pip + venv + pip-tools merged.

`uv_build` currently only supports pure Python code. It integrates tightly with `uv`. However `uv` supports all build backends (as specified by PEP 517).

## Current Repo Decision

For the mixed Rust/Python experiment, `maturin` is sufficient because its mixed layout can place the native extension inside the Python package source tree. This means there is no current need to switch to `setuptools + setuptools-rust`.
