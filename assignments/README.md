# Assignments

This directory contains course assignment repos and code.

For assignment work, the agent acts as a teaching assistant: explain, review, suggest checks, and help debug without directly solving core assignment tasks.

## Layout

Preserve each original assignment repo root inside a subdirectory:

```text
assignments/
└── assignment1-basics/
    ├── pyproject.toml
    ├── uv.lock
    ├── cs336_basics/
    └── tests/
```

Run assignment commands from that assignment directory, for example:

```bash
cd assignments/assignment1-basics
uv run pytest
```

Do not merge multiple assignments' packages and tests into the repository root.

## Cross-Assignment Dependencies

Some later assignments may depend on earlier assignment packages, such as `cs336-systems` depending on `cs336-basics`.

Prefer either:

- independent assignment projects with a local path dependency from the later assignment to the earlier one; or
- a uv workspace if the assignments have compatible Python/dependency requirements and one shared lockfile is acceptable.

More details live in `notes/tools/uv.md`.

## Agent Boundary

- Do not complete TODOs, implement core assignment components, or directly solve assignment problems.
- Do not edit assignment code unless the owner explicitly asks for a non-core mechanical change.
- If reviewing code the owner wrote, point to likely issues, missing checks, edge cases, or relevant tests without providing a finished solution.
- Follow any nested `AGENTS.md` file inside an assignment directory.
