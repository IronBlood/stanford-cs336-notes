# Foreign function interface (FFI)

FFI is a mechanism that allows one programming language to call functions implemented in another programming language.

## Why it is useful

High-level programming languages usually provide convenient features such as cross-platform support, object-oriented programming (OOP) and garbage collection (GC). Programmers don't need to deal with low-level system-related details directly. However the trade-off is that some high-level programming languages can be less efficient for certain workloads, depending on implementation, runtime and workload.

FFI allows programmers to implement functions in low-level programming languages (usually C, C++ and Rust), then invoke them from other programming languages such as Java, Node.js, Ruby and Python.

FFI does not automatically make code faster. Crossing the language boundary has overhead, so FFI is most useful when the lower-level function does enough work to justify that cost. At the lower level, programmers have the ability to invoke more powerful APIs (for example CUDA and video decoding). FFI can combine programmer productivity with low-level runtime performance.
