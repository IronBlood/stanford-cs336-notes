---
type: concept
status: stub
course: cs336
tags: [language-models, pretrained-models]
---

# BERT

BERT stands for Bidirectional Encoder Representations from Transformers. It is a pre-trained Transformer-based language model that was commonly downloaded and fine-tuned for downstream NLP tasks before the current style of large generative language models became dominant.

## Why It Matters

In [Lecture 1](../lectures/01-overview.md), BERT appears as an example of the earlier workflow around language models:

1. Start from a model already pre-trained on a large corpus.
2. Fine-tune it on a task-specific dataset.
3. Deploy the fine-tuned model for a specific NLP task.

This is useful context for understanding how the field moved from task-specific fine-tuning toward more general-purpose generative models and prompting.

## Current Understanding

- BERT is based on the Transformer architecture.
- Unlike autoregressive language models that predict the next token left-to-right, BERT is associated with masked language modeling: predict hidden tokens from surrounding context.
- It is often described as an encoder-style model rather than a decoder-style generative model.

## Questions

- What is a Transformer, and what does it mean for BERT to be "Transformer-based"?
- What exactly is the difference between encoder-only, decoder-only, and encoder-decoder Transformers?
- Why did masked language modeling work well for BERT-style pre-training?
- Which parts of the BERT workflow still matter for modern language models?

## Sources

- Mentioned in [Lecture 1](../lectures/01-overview.md) from `raw/transcripts/01-overview.md`.
- Needs source: original BERT paper.
