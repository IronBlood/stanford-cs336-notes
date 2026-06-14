---
type: tool
status: draft
course: cs336
tags: [python, tooling]
---

# uv

`uv` is a Python project and package management tool. In this repo, use it to manage the Python environment for experiments, assignment code, and small scripts.

The working assumption for this repo: initialize one project at the repository root so dependencies can be shared across different experiment folders.

## Project Setup

Initialize the repo as a uv project from the repository root:

```bash
uv init --vcs none .
```

Meaning:

- `.` means initialize the current directory instead of creating a new subdirectory.
- `--vcs none` tells uv not to initialize version control files. This repo is already managed by git, so uv does not need to create a new VCS setup.

This creates project files such as:

```text
pyproject.toml
uv.lock
.python-version
```

For this repo, a root-level project is simpler than one Python project per experiment. It means scripts in different folders can share the same dependencies.

Possible layout:

```text
.
├── pyproject.toml
├── uv.lock
├── experiments/
│   ├── tokenizer/
│   │   └── explore_bpe.py
│   └── tensors/
│       └── shapes.py
├── assignments/
│   └── assignment-01/
│       └── ...
└── notes/
```

## Managing Packages

Add a package:

```bash
uv add numpy
```

Add a version constraint:

```bash
uv add "numpy>=2"
```

Remove a package:

```bash
uv remove numpy
```

These commands update `pyproject.toml` and the lockfile.

For tools used only during development, use a dependency group:

```bash
uv add --group lint ruff
uv add --group test pytest
```

For this repo, start simple: put common experiment dependencies in the main project dependencies. Use groups later if the environment becomes noisy.

## Running Scripts

Run a script inside the project environment:

```bash
uv run python experiments/tensors/shapes.py
```

Or:

```bash
uv run experiments/tensors/shapes.py
```

Using `uv run` matters because the project environment is isolated from the shell. If a script imports a package from the uv project, run it through `uv run`.

## Folder Names And Imports

Python folder names matter more than in many Node.js workflows.

For simple experiments, avoid relying on cross-folder imports at first. Prefer scripts that can run from the repository root:

```bash
uv run python experiments/tokenizer/explore_bpe.py
```

If a folder needs to behave like an importable Python package, it usually needs:

```text
some_package/
└── __init__.py
```

But for early learning experiments, do not over-package everything. A plain script in a clearly named folder is usually enough.

Good beginner rule:

- Use folders to organize experiments.
- Run scripts from the repository root.
- Keep shared reusable code rare at first.
- When code is reused by multiple experiments, then consider making a small package/module.

## One-Off Dependencies

For a temporary dependency without adding it to the project:

```bash
uv run --with rich python scratch/demo.py
```

This can be useful for quick experiments, but for course work it is usually better to add real dependencies with `uv add` so the environment is reproducible.

## Repo Convention

- Root `pyproject.toml`: shared dependency set for course experiments and assignments.
- `experiments/`: small exploratory scripts split by topic.
- `assignments/`: course assignment code.
- `notes/`: wiki notes; not Python package code.
- `scratch/`: temporary files and throwaway experiments.

## Questions

- Should assignments share the root uv project, or should a specific assignment have its own project if the course requires exact dependencies?
- When should repeated experiment code become a real Python module?
- How should PyTorch dependencies be added, especially if CUDA-specific installation matters?

## Sources

- [uv docs: Creating projects](https://docs.astral.sh/uv/concepts/projects/init/)
- [uv docs: Managing dependencies](https://docs.astral.sh/uv/concepts/projects/dependencies/)
- [uv docs: Running commands in projects](https://docs.astral.sh/uv/concepts/projects/run/)
- [uv docs: Running scripts](https://docs.astral.sh/uv/guides/scripts/)
