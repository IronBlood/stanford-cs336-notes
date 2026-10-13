# Lecture 5: GPUs, TPUs

## Keywords

- GPU memory hierarchy
- Arithmetic intensity
- Kernel fusion
- Tiling
- FlashAttention

## Summary

The lecture explains GPUs as throughput-oriented processors and relates threads, warps, and blocks to streaming multiprocessors and their memory hierarchy. A comparison with TPUs highlights shared principles and differences in execution granularity. Arithmetic intensity and the roofline model explain why memory movement often limits performance. Optimization techniques include reducing precision, recomputation, kernel fusion, coalesced memory access, and tiling. Matrix dimensions and tile scheduling explain seemingly surprising throughput changes, including alignment effects and wave quantization. FlashAttention brings these ideas together: tiled computation, online softmax, fusion, and backward recomputation reduce memory traffic without materializing the full attention matrix in global memory.

Source: [YouTube transcript](../../raw/transcripts/Stanford%20CS336%20Language%20Modeling%20from%20Scratch%20%EF%BD%9C%20Spring%202026%20%EF%BD%9C%20Lecture%205%EF%BC%9A%20GPUs%2C%20TPUs-izZba4UA7iY.en-US.srt).

