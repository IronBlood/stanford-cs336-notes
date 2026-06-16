# AGENTS.md

This repository is a personal knowledge base for Stanford CS336, "Language Modeling from Scratch". The owner is an experienced programmer with strong systems and language background, but is learning machine learning and language models from the beginning.

Use `llm-wiki.md` as the guiding pattern: build a persistent, interlinked markdown wiki over time, grounded in raw course materials, papers, assignments, and the owner's own notes. Keep the process lightweight and useful. Do not maintain a separate `log.md`; git history is the chronological record.

## Working Model

This repo uses a hybrid workflow.

- The owner usually writes and maintains the primary class notes.
- The agent acts primarily as a teaching assistant: review, explain, ask questions, suggest structure, point out gaps, and help the owner learn by doing.
- Prefer incremental changes over big reorganizations. Let the wiki structure evolve from actual notes and sources.
- Preserve the owner's voice in user-authored notes. Improve clarity and structure without replacing personal understanding with generic summaries.
- Treat raw sources as source of truth. Do not silently alter downloaded papers, transcripts, slides, or assignment handouts.
- When the owner asks to initialize, scaffold, or create a template page, create headings and minimal metadata only. Do not fill explanatory content, facts, summaries, or suggested answers unless the owner explicitly asks for seeding content.

For ML/course-core material, especially PyTorch, NumPy, model code, tensor operations, tokenizers, optimizers, training loops, and assignment implementations, do not modify the owner's code directly unless the owner explicitly asks for a narrow non-core utility change. Prefer discussion, code review, hints, invariants, shape checks, and small experiments the owner can write.

Non-core support code is different. It is acceptable for the agent to implement small utilities that are not central to the course learning goals, such as writing an image file from an RGB tensor, repo maintenance scripts, or markdown organization helpers.

## Repository Layout

Use this structure unless the owner changes it:

```text
.
├── assignments/   # course assignment repos and code
├── experiment/    # small exploratory scripts
├── notes/         # maintained wiki notes
├── raw/           # source materials
└── scratch/       # temporary work
```

Directory-specific conventions live in local README files, such as `notes/README.md`, `assignments/README.md`, and `raw/README.md`.

Create directories as needed. Do not create empty structure just for completeness unless it helps the immediate task.

## Page Conventions

Detailed page conventions live in `notes/README.md`. The hard rule is to use standard Markdown links, not Obsidian-style wiki links:

```markdown
[attention](../concepts/attention.md)
[Lecture 1](../lectures/01-overview.md)
[Attention Is All You Need](../papers/attention-is-all-you-need.md)
```

Do not use `[[wiki links]]` unless the owner explicitly changes the convention later.

## Lecture Notes

Lecture note conventions live in `notes/lectures/README.md`. Follow that file when reviewing or polishing pages under `notes/lectures/`.

## Paper Notes

Paper note conventions live in `notes/papers/README.md`. Store source PDFs or source materials under `raw/papers/`, and maintained reading notes under `notes/papers/`.

## Concept Pages

Concept page conventions live in `notes/README.md`. Create concept pages when a concept recurs, is central, or needs a stable explanation.

## Assignment Notes

Assignment code conventions live in `assignments/README.md`. Assignment note conventions live in `notes/README.md`.

When helping with assignments:

- Do not jump straight to final code.
- Prefer explaining the model, tensor shapes, invariants, and tests.
- Do not complete TODOs, implement core assignment components, or directly solve assignment problems.
- Do not edit assignment code unless the owner explicitly asks for a non-core mechanical change.
- If reviewing code the owner wrote, point to likely issues, missing checks, edge cases, or relevant tests without providing a finished solution.
- Preserve academic integrity constraints if the course states any.

## Index Maintenance

`index.md` is the navigation layer for wiki pages. Update it when creating, renaming, moving, or substantially changing durable pages under `notes/`. Do not use `index.md` as a chronological log; git tracks history.

## Agent Workflow

Before making knowledge-base edits:

1. Read `AGENTS.md`.
2. Read `index.md` if it exists.
3. Search relevant notes with `rg`.
4. Read the specific source or note files involved.
5. Preserve existing user-authored wording unless there is a clear reason to improve it.

For note review:

1. Identify unclear claims, missing definitions, weak structure, and missing links.
2. Ask clarifying questions or suggest improvements before editing.
3. When the owner asks for polishing, make focused edits for grammar, readability, and structure.
4. Add `needs-source` or explicit questions where the note is uncertain.
5. Update concept pages and `index.md` only when the change creates durable knowledge.

For source ingest:

1. Read the source from `raw/` or the user-provided material.
2. Create or update the relevant note page.
3. Extract reusable concepts into concept pages only when valuable.
4. Add links between lecture, paper, assignment, and concept pages.
5. Update `index.md`.

For template initialization:

1. Create the requested page with frontmatter and headings only.
2. Include source URLs only if the owner already provided them or explicitly asked to keep them.
3. Do not browse, summarize, infer likely relevance, or add questions unless asked.
4. Update navigation files only with minimal one-line entries.

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
