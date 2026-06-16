---
type: dataset
status: draft
course: cs336
tags: [datasets, language-modeling]
---

# TinyStories

> **NOTE**: This page is about the dataset, for paper related notes, see [papers/tiny-stories.md](../papers/tiny-stories.md).

This repo contains both the original data in [parquet](../concepts/parquet.md) format, and splitted text files for training and validation. There is no need to download the whole repo using `hf`, `wget(1)` is enough, see more from [README.md from assignment 1](../../assignments/assignment1-basics/README.md):

```
wget https://huggingface.co/datasets/roneneldan/TinyStories/resolve/main/TinyStoriesV2-GPT4-train.txt
wget https://huggingface.co/datasets/roneneldan/TinyStories/resolve/main/TinyStoriesV2-GPT4-valid.txt
```

Then there are:

- `TinyStoriesV2-GPT4-train.txt` 2.2G
- `TinyStoriesV2-GPT4-valid.txt` 23M

## Sources

- [Hugging Face: roneneldan/TinyStories](https://huggingface.co/datasets/roneneldan/TinyStories)
