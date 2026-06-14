# AGENTS.md

This repository is a personal knowledge base for Stanford CS336, "Language Modeling from Scratch". The owner is an experienced programmer with strong systems and language background, but is learning machine learning and language models from the beginning.

Use `llm-wiki.md` as the guiding pattern: build a persistent, interlinked markdown wiki over time, grounded in raw course materials, papers, assignments, and the owner's own notes. Keep the process lightweight and useful. Do not maintain a separate `log.md`; git history is the chronological record.

## Working Model

This repo uses a hybrid workflow.

- The owner usually writes and maintains the primary class notes.
- The agent helps with review, explanation, restructuring, cross-linking, paper reading, and consistency checks.
- Prefer incremental changes over big reorganizations. Let the wiki structure evolve from actual notes and sources.
- Preserve the owner's voice in user-authored notes. Improve clarity and structure without replacing personal understanding with generic summaries.
- Treat raw sources as source of truth. Do not silently alter downloaded papers, transcripts, slides, or assignment handouts.

## Repository Layout

Use this structure unless the owner changes it:

```text
.
├── AGENTS.md
├── llm-wiki.md
├── index.md
├── assignments/
├── notes/
│   ├── lectures/
│   ├── concepts/
│   ├── papers/
│   ├── assignments/
│   ├── tools/
│   └── questions/
├── raw/
│   ├── papers/
│   ├── slides/
│   ├── transcripts/
│   ├── assignments/
│   └── assets/
└── scratch/
```

- `index.md`: content-oriented map of the wiki. Update when adding or substantially reorganizing pages.
- `assignments/`: code for course assignments. Use one subdirectory per assignment, such as `assignments/assignment-01/`.
- `notes/lectures/`: class-by-class notes from videos or live materials.
- `notes/concepts/`: durable concept pages, such as tokenization, transformers, attention, backpropagation, optimization, scaling laws, evaluation, and inference.
- `notes/papers/`: paper summaries and reading notes.
- `notes/assignments/`: assignment writeups, implementation notes, debugging records, and conceptual takeaways.
- `notes/tools/`: notes about tools used for the course, such as Python packaging, `uv`, notebooks, or command-line utilities.
- `notes/questions/`: useful Q&A, comparisons, explanations, and unresolved confusions worth keeping.
- `raw/`: immutable or mostly immutable source files. The agent may read but should not rewrite these unless explicitly asked.
- `scratch/`: temporary drafts, experiments, extracted text, and intermediate analysis. Anything here may be messy.

Create directories as needed. Do not create empty structure just for completeness unless it helps the immediate task.

## Page Conventions

Prefer concise vanilla Markdown pages that render well on GitHub and are easy to search with command-line tools.

Use standard Markdown links for internal references:

```markdown
[attention](../concepts/attention.md)
[Lecture 1](../lectures/01-overview.md)
[Attention Is All You Need](../papers/attention-is-all-you-need.md)
```

Do not use Obsidian-style `[[wiki links]]` unless the owner explicitly changes the convention later.

Use lowercase kebab-case filenames:

```text
notes/concepts/self-attention.md
notes/papers/attention-is-all-you-need.md
notes/lectures/lecture-01-overview.md
```

Use YAML frontmatter when it adds useful structure:

```yaml
---
type: concept
status: draft
course: cs336
tags: [language-models]
---
```

Recommended `type` values:

- `lecture`
- `concept`
- `paper`
- `assignment`
- `question`
- `index`

Recommended `status` values:

- `stub`: placeholder or incomplete page
- `draft`: useful but still rough
- `reviewed`: checked by the owner or against sources
- `needs-source`: claim needs a citation or raw source

## Lecture Notes

For class-by-class notes, prefer this shape:

```markdown
# Lecture N: Title

## Big Picture

## Key Ideas

## Terms

## Details

## Connections

## Questions

## Sources
```

Do not force every section if it would be empty. For early notes, it is fine to keep rough bullets and mark uncertainty explicitly.

When reviewing lecture notes:

- Explain ML-specific concepts from first principles when needed.
- Connect new ideas to systems/programming analogies only when the analogy is accurate.
- Flag analogies that are useful but leaky.
- Split pages only when the lecture note becomes hard to navigate or introduces reusable concepts.
- Promote reusable explanations into `notes/concepts/` and link back from the lecture.

## Paper Notes

For papers, store the PDF or source material under `raw/papers/` and the maintained note under `notes/papers/`.

Prefer this shape:

```markdown
# Paper Title

## Citation

## Why This Matters

## Problem

## Core Idea

## Method

## Results

## Limitations

## Connections

## Questions

## Source
```

When helping read papers:

- Start with the motivation and problem statement before equations.
- Separate what the paper claims from what later work or the course says.
- Translate unfamiliar ML notation into programming-oriented language when useful.
- Keep mathematical details, but do not let them obscure the main mechanism.
- Mark unresolved confusions rather than smoothing them over.

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

Assignment notes may include implementation plans, pitfalls, debugging findings, and conceptual takeaways. Keep actual assignment code under `assignments/` unless the course provides a required layout.

When helping with assignments:

- Do not jump straight to final code if the owner is trying to learn the concept.
- Prefer explaining the model, tensor shapes, invariants, and tests.
- When editing assignment code, keep changes inside the relevant `assignments/assignment-N/` directory unless shared utilities are clearly needed.
- Preserve academic integrity constraints if the course states any.

## Index Maintenance

`index.md` is the navigation layer. It should list maintained wiki pages with one-line summaries, grouped by category.

Update `index.md` when:

- Creating a durable page under `notes/`.
- Renaming or moving a page.
- Substantially changing the meaning or status of a page.

Do not use `index.md` as a chronological log. Git tracks history.

## Agent Workflow

Before making knowledge-base edits:

1. Read `AGENTS.md`.
2. Read `index.md` if it exists.
3. Search relevant notes with `rg`.
4. Read the specific source or note files involved.
5. Preserve existing user-authored wording unless there is a clear reason to improve it.

For note review:

1. Identify unclear claims, missing definitions, weak structure, and missing links.
2. Suggest or make focused edits.
3. Add `needs-source` or explicit questions where the note is uncertain.
4. Update concept pages and `index.md` only when the change creates durable knowledge.

For source ingest:

1. Read the source from `raw/` or the user-provided material.
2. Create or update the relevant note page.
3. Extract reusable concepts into concept pages only when valuable.
4. Add links between lecture, paper, assignment, and concept pages.
5. Update `index.md`.

For queries:

1. Search the wiki first.
2. Answer from existing notes when possible.
3. If the answer reveals a durable explanation, ask or infer whether it should become a page under `notes/questions/` or `notes/concepts/`.
4. Cite local files and source materials clearly.

For linting:

- Look for orphan pages, missing backlinks, duplicated explanations, stale claims, unresolved questions, and important concepts without pages.
- Prefer a short actionable report over large automatic rewrites.
- Make structural changes only when they are clearly beneficial.

## Style

- Be precise and compact.
- Prefer concrete examples, tensor shapes, pseudocode, and implementation invariants over vague descriptions.
- State uncertainty explicitly.
- Distinguish course explanation, paper claim, implementation note, and personal interpretation.
- Avoid unnecessary polish that hides rough learning state.
- Do not add decorative content, motivational summaries, or generic study advice.
