# Lecture 6: Kernels, Triton, XLA

## Keywords

- GPU programming
- Benchmarking and profiling
- Triton
- Kernel fusion
- Tiled matrix multiplication

## Summary

The lecture turns the GPU hardware model into practical programming and measurement. It examines how warps, register use, bank conflicts, memory coalescing, and occupancy affect performance. Reliable benchmarking requires warmup and synchronization; profiling reveals which kernels high-level tensor operations actually invoke. Comparing naive, built-in, and compiled GELU implementations shows the benefit of kernel fusion. Triton examples progress from elementwise operations to row-wise softmax, reductions that exceed a block's capacity, and tiled matrix multiplication. The block-oriented abstraction simplifies programming, while generated PTX exposes lower-level execution. The main workflow is to measure bottlenecks, change the implementation, and measure again.

Source: [YouTube transcript](../../raw/transcripts/Stanford%20CS336%20Language%20Modeling%20from%20Scratch%20%EF%BD%9C%20Spring%202026%20%EF%BD%9C%20Lecture%206%EF%BC%9A%20Kernels%2C%20Triton%2C%20XLA-xnDHaNUvHBg.en-US.srt).

