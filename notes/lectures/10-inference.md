# Lecture 10: Inference

## Keywords

- Prefill and decoding
- KV cache
- Arithmetic intensity
- Speculative decoding
- PagedAttention

## Summary

The lecture analyzes inference through time to first token, per-request latency, and aggregate throughput. Prefill processes known prompt tokens in parallel, whereas autoregressive decoding generates tokens sequentially and reuses cached keys and values. FLOP and memory accounting explain why decoding is often memory-bound and why larger batches trade latency for throughput. Architectural techniques such as grouped-query, latent, local, and linear attention reduce KV-cache costs. Quantization, pruning, and distillation offer additional efficiency tradeoffs. Speculative decoding uses a cheaper draft model with target-model verification, while PagedAttention manages cache allocation and sharing. The goal is faster serving with carefully checked effects on output quality.

Source: [YouTube transcript](../../raw/transcripts/Stanford%20CS336%20Language%20Modeling%20from%20Scratch%20%EF%BD%9C%20Spring%202026%20%EF%BD%9C%20Lecture%2010%EF%BC%9A%20Inference-EfM546A79aM.en-US.srt).

