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
│   └── assignment1-basics/
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

## Multiple Course Assignments

The Stanford assignment repos are Python projects. For example, the first assignment repo root contains files like:

```text
uv.lock
pyproject.toml
cs336_basics/
tests/
```

In this notes repo, map each original assignment repo root into its own subdirectory:

```text
assignments/
└── assignment1-basics/
    ├── uv.lock
    ├── pyproject.toml
    ├── cs336_basics/
    └── tests/
```

Then run the assignment's commands from that directory:

```bash
cd assignments/assignment1-basics
uv run pytest
```

This preserves the assignment's expected import paths and test setup.

Do not put all assignments' `cs336_*` packages and `tests/` directories directly under the repo root. That would make names collide and make it harder to reproduce the course instructions.

### Assignment Dependencies

Some assignments may depend on earlier assignments.

For example, assignment 1 declares the package:

```toml
[project]
name = "cs336_basics"
```

Assignment 2 may declare:

```toml
[project]
name = "cs336-systems"
dependencies = [
    "cs336-basics",
]
```

The underscore vs hyphen difference is normal in Python package metadata: distribution names are commonly normalized, so `cs336_basics` and `cs336-basics` refer to the same package name for dependency resolution.

This means the assignments are not just unrelated folders. Later assignments may need earlier assignment code to be installable.

### Why Not One Flat Root Project?

A flat root project would look like this:

```text
.
├── pyproject.toml
├── uv.lock
├── cs336_basics/
├── tests/
└── ...
```

That is close to the original assignment repo, but it only works cleanly for one assignment at a time. As soon as there are multiple assignments, root-level package names, test folders, and dependency versions may conflict.

### uv Workspace Option

`uv` also supports workspaces, where multiple packages live in one repository and share one lockfile. That is closer to pnpm/yarn workspace terminology.

This can fit the CS336 assignments if they are meant to build on each other and have compatible dependency requirements.

A possible layout:

```text
.
├── pyproject.toml
├── uv.lock
└── assignments/
    ├── assignment1-basics/
    │   ├── pyproject.toml
    │   ├── cs336_basics/
    │   └── tests/
    └── assignment2-systems/
        ├── pyproject.toml
        ├── cs336_systems/
        └── tests/
```

Root `pyproject.toml` would include:

```toml
[tool.uv.workspace]
members = ["assignments/assignment*"]
```

Then assignment 2 can point its `cs336-basics` dependency at the workspace member:

```toml
[tool.uv.sources]
cs336-basics = { workspace = true }
```

Run tests for a specific package from the workspace root:

```bash
uv run --package cs336-systems pytest
```

Or from the assignment directory:

```bash
cd assignments/assignment2-systems
uv run pytest
```

The benefit: the assignment packages can depend on each other locally, and uv manages one consistent environment.

The cost: a workspace shares one lockfile and effectively one resolved dependency set. That is less isolated than preserving each assignment's original `uv.lock`.

### Independent Projects With Path Dependencies

If preserving each assignment's original lockfile matters more, keep each assignment as an independent uv project and add a local path source in the later assignment.

For example, in `assignments/assignment2-systems/pyproject.toml`:

```toml
[tool.uv.sources]
cs336-basics = { path = "../assignment1-basics", editable = true }
```

Then run:

```bash
cd assignments/assignment2-systems
uv run pytest
```

This keeps assignment 2 independent while still allowing it to import assignment 1 as a local package.

### Rule Of Thumb

Start with independent assignment folders. When a later assignment actually depends on an earlier package, choose:

- Path dependency: best when preserving the original assignment lockfiles and isolation matters.
- uv workspace: best when assignments are meant to be developed together and compatible dependencies are expected.

## Questions

- Should assignment dependencies use local path sources or a uv workspace?
- When should repeated experiment code become a real Python module?
- How should PyTorch dependencies be added, especially if CUDA-specific installation matters?

## Sources

- [uv docs: Creating projects](https://docs.astral.sh/uv/concepts/projects/init/)
- [uv docs: Managing dependencies](https://docs.astral.sh/uv/concepts/projects/dependencies/)
- [uv docs: Running commands in projects](https://docs.astral.sh/uv/concepts/projects/run/)
- [uv docs: Running scripts](https://docs.astral.sh/uv/guides/scripts/)
- [uv docs: Using workspaces](https://docs.astral.sh/uv/concepts/projects/workspaces/)
