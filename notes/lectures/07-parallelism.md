# Lecture 7: Parallelism

## Keywords

- Collective communication
- GPU interconnects
- Data parallelism
- Tensor parallelism
- Pipeline parallelism

## Summary

The lecture introduces multi-GPU programming as another problem of moving data efficiently through a hardware hierarchy. It defines ranks and world size, then explains collective operations, especially all-reduce, reduce-scatter, and all-gather. GPU networking and NCCL connect these abstractions to physical communication, while PyTorch examples demonstrate synchronization and bandwidth measurement. Simple MLP training examples illustrate three strategies: data parallelism splits examples and synchronizes gradients, tensor parallelism splits layer computations, and pipeline parallelism assigns layers to different devices. Microbatches reduce pipeline idle time. Choosing and combining strategies depends on memory capacity, interconnect speed, batch size, and opportunities to overlap communication with computation.

Source: [YouTube transcript](../../raw/transcripts/Stanford%20CS336%20Language%20Modeling%20from%20Scratch%20%EF%BD%9C%20Spring%202026%20%EF%BD%9C%20Lecture%207%EF%BC%9A%20Parallelism-SzpOcwdIL0Y.en-US.srt).

