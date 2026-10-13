# Guest Lecture: Dan Fu

## Keywords

- Inference serving
- Continuous batching
- Cache-aware routing
- Megakernels
- Looped transformers

## Summary

Dan Fu follows the lifetime of a token through an inference service, connecting workload characteristics to scheduling, batching, caching, and GPU execution. Prefill and decoding have different bottlenecks, motivating separate workers and cache-aware routing. KV-cache storage becomes a hierarchy spanning GPUs, CPU memory, and disks, with eviction and locality affecting performance. Megakernels fuse larger portions of model execution and schedule dependent work to reduce launch overhead and idle time, at substantial engineering cost. The Parcae discussion explores stabilized looped transformers and scaling recurrence alongside data and parameters. The broader argument is that understanding serving systems enables coordinated improvements to hardware use, kernels, and model architecture.

Source: [YouTube transcript](../../raw/transcripts/Stanford%20CS336%20Language%20Modeling%20from%20Scratch%20%EF%BD%9C%20Spring%202026%20%EF%BD%9C%20Guest%20Lecture%EF%BC%9A%20Dan%20Fu-9EEm4iMAF5s.en-US.srt).

