# Notes

This directory contains the maintained wiki layer for the course.

The owner writes first. The agent reviews, asks questions, suggests structure and links, and only edits when asked to polish or reorganize.

## Layout

```text
notes/
├── lectures/      # class-by-class notes
├── concepts/      # reusable explanations
├── datasets/      # dataset notes
├── papers/        # paper reading notes
├── assignments/   # assignment writeups and debugging notes
├── tools/         # uv, Python tooling, environment notes
└── questions/     # durable Q&A and unresolved confusions
```

## Page Conventions

- Use concise vanilla Markdown that renders well on GitHub.
- Use standard Markdown links, not Obsidian-style wiki links.
- Use lowercase kebab-case filenames.
- Use YAML frontmatter when it adds useful structure.

Recommended `type` values:

- `lecture`
- `concept`
- `paper`
- `dataset`
- `assignment`
- `tool`
- `question`
- `index`

Recommended `status` values:

- `stub`: placeholder or incomplete page
- `draft`: useful but still rough
- `reviewed`: checked by the owner or against sources
- `needs-source`: claim needs a citation or raw source

## Concept Pages

Concept pages are durable explanations that can be improved across lectures, papers, and assignments.

Good concept pages should include:

- A short definition.
- Why the concept matters for language models.
- The operational or implementation view.
- Important equations or pseudocode when relevant.
- Links to lectures, papers, assignments, and related concepts.
- Common confusions and edge cases.

Avoid making a concept page for every term too early. Create one when a concept recurs, is central, or needs a stable explanation.

## Assignment Notes

`notes/assignments/` is for writeups, implementation notes, debugging records, and conceptual takeaways.

Keep actual assignment code under `assignments/`.

## Directory READMEs

- `notes/lectures/README.md`: lecture note conventions.
- `notes/papers/README.md`: paper note conventions.
- `notes/tools/uv.md`: uv and Python project notes.
