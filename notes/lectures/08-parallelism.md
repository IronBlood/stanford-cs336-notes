# Lecture 8: Parallelism

## Keywords

- ZeRO and FSDP
- Tensor and sequence parallelism
- Pipeline scheduling
- Expert and context parallelism
- Communication overlap

## Summary

The lecture expands basic parallelism into strategies for training large models across clusters. Memory accounting motivates ZeRO's progressive sharding of optimizer state, gradients, and parameters, including fully sharded data parallelism. Model parallel approaches address remaining limits: tensor and sequence parallelism reduce local computation or activations, pipeline schedules manage idle periods, and expert or context parallelism handle sparse models and long sequences. Each method trades memory, communication, and usable batch size differently. Combining them requires matching frequent communication to fast links and hiding transfers behind computation. Published training configurations illustrate practical choices, including why no single parallelization strategy dominates every workload.

Source: [YouTube transcript](../../raw/transcripts/Stanford%20CS336%20Language%20Modeling%20from%20Scratch%20%EF%BD%9C%20Spring%202026%20%EF%BD%9C%20Lecture%208%EF%BC%9A%20Parallelism-6-cXp-aOmdg.en-US.srt).

