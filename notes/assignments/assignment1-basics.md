# Assignment 1: Basics

## Chapter 2
### Problem unicode1a

> What Unicode character does `chr(0)` return?

It returns `U+0000`, the null character.

### Problem unicode1b

> How does this character's string representation `(__repr__())` differ from its printed representation?

`print` writes the actual character to stdout. Since `U+0000` is not printable, the terminal usually shows no visible glyph for it. `repr()` returns a debugging representation of the string, so it escapes the null character as `\x00`.

### Problem unicode1c

> What happens when this character occurs in text? It may be helpful to play around with the following in your Python intepreter and see if it  matches your expectations:
>
> ```
> >>> chr(0)
> >>> print(chr(0))
> >>> "a" + chr(0) + "b"
> >>> print("a" + chr(0) + "b")
> ```

The character is inserted in the string as-is. Python does not treat it as a terminator as in C. It remains part of the string even though it is usually invisible when printed.

### Problem unicode2a

> What are some reasons to prefer training out tokenizer on UTF-8 encoded bytes, rather than UTF-16 or UTF-32? It may be helpful to compare the output of these encodings for various input strings.

Short answer:

UTF-8 is prefered because it is the dominant text encoding on the web and it's compact while still being able to represent all Unicode characters. UTF-16 and UTF-32 often introduce extra zero bytes or longer byte sequences for the same text, which makes byte-level tokenization less efficient and wastes tokenizer capacity on encoding artifacts.

### Problem unicode2b

> Consider the following (incorrect) function, which is intended to decode a UTF-8 byte string into a Unicode string. Why is this function incorrect? Provide an example of an input byte string that yields incorrect results.
>
> ```python
> def decode_utf8_bytes_to_str_wrong(bytestring: bytes):
>     return "".join([bytes([b]).decode("utf-8") for b in bytestring])
> decode_utf8_bytes_to_str_wrong("hello".encode("utf-8"))
> ```

The function tries to decode byte by byte. It works for the example input, which are bytes for `"hello"`. Each character also falls into the ASCII code, which is compatible with UTF-8. However there are characters, for example Chinese, Japanese, or `é` which require multiple bytes, decoding byte by byte will fail.

### Problem unicode2c

> Give a two-byte sequence that does not decode to any Unicode character(s).

`b"\xFF\xFF"` does not decode to any Unicode character(s).

### Problem train_bpe

> Write a function that, given a path to an input text file, trains a (byte-level) BPE
> tokenizer. Your BPE training function should handle (at least) the following input parameters:
>
> **Input**
>
> - `input_path`: `str` Path to a text file with BPE tokenizer training data.
> - `vocab_size`: `int` A positive integer that defines the maximum final vocabulary size (including the initial byte vocabulary, vocabulary items produced from merging, and any special tokens).
> - `special_tokens`: `list[str]` A list of strings to add to the vocabulary. During training, treat them as hard boundaries that prevent merges across their spans, but do not include them when computing merge statistics.
>
> Your BPE training function should return the resulting vocabulary and merges:
>
> **Output**
>
> - `vocab`: `dict[int, bytes]` The tokenizer vocabulary, a mapping from int (token ID in the vocabulary) to bytes (token bytes).
> - `merges`: `list[tuple[bytes, bytes]]` A list of BPE merges produced from training. Each list item is a tuple of bytes `(<token1>, <token2>)`, representing that `<token1>` was merged with `<token2>`. The merges should be ordered by order of creation.
>
> To test your BPE training function against our provided tests, you will first need to implement the test adapter at `adapters.run_train_bpe`. Then, run `uv run pytest tests/test_train_bpe.py`. Your implementation should be able to pass all tests. Optionally (this could be a large time-investment), you can implement the key parts of your training method using some systems language, for instance C++ (consider `cppyy` or `nanobind`) or Rust (using `PyO3`). If you do this, be aware of which operations require copying vs reading directly from Python memory, and make sure to leave build instructions, or make sure it builds using only `pyproject.toml`. Also note that the GPT-2 regex is not well-supported in most regex engines and will be too slow in most that do. We have verified that Oniguruma is reasonably fast and supports negative lookahead, but the regex package in Python is, if anything, even faster.

#### Notes for `pretokenization_example.py`

The example in [pretokenization_example.py](../../assignments/assignment1-basics/cs336_basics/pretokenization_example.py) divides a file into smaller chunks whose boundaries are aligned with a special token:

1. It calculates approximately even byte-offset guesses using `file_size // desired_num_chunks`.
2. For each internal guess, it searches forward in blocks of up to 4 KiB for the next complete occurrence of the special token.
3. It replaces the guessed boundary with the byte offset where that special token begins. If no special token is found before EOF, it moves the boundary to EOF.
4. It removes duplicate boundaries and pairs adjacent boundaries to define the byte range of each chunk.
5. It reads each range as bytes and then decodes it as UTF-8 for pre-tokenization. Because a boundary points to the first byte of a special token, that token begins the following chunk.

#### Implementation and Test Results

The whole implementation contains three layers:

1. (Python) The entrance: [bpe.py](../../assignments/assignment1-basics/cs336_basics/bpe.py) calls the native extension
2. (PyO3) The Python/Rust glue layer: [lib.rs](../../assignments/assignment1-basics/src/lib.rs) handles the parameters from Python, calls the actual implementation and then prepares the final data format.
3. (Rust) The implementation: [util.rs](https://github.com/IronBlood/cs336-rs/blob/bf5ce8f8adaddaa091f91974e494760c3948c290/src/utils.rs)

All three tests passed. With `dev` profile (unoptimized + debuginfo), `test_train_bpe_speed` takes 0.11s; switching to `release` profile (optimized), `test_train_bpe_speed` takes 0.05s.

> NOTE: The reference implementation takes 0.38s on the lecturer's laptop, and the test requires the runtime to be finished within 1.5s. The [first bug-fixed Rust implementation](https://github.com/IronBlood/cs336-rs/commit/550e15058dd7ea2ed263ea1487dd3a7e26fac145) takes about 2s with `dev` profile, 0.2s with `release` profile.

#### Why Rust is Used

BPE tokenizer training doesn't invoke any PyTorch operations, it is pure string and byte level operations. The tokenizer will later be used on the TinyStories dataset and the OpenWebText dataset. The OpenWebText dataset is about 12G, while the TinyStories dataset is smaller, but still 2.2G. String is a built-in type in Python. When doing string operations, such as `text[start:end]` and `text.split(",")`, new string objects are created, and extra spaces are allocated to store the copied data.

> NOTE: Python has an API `memoryview()`, a zero-copy mechanism to view over bytes-like buffers. Due to my limited Python experience, this doesn't seem a direct solution for Python `str` slicing.

Rust, on the other hand, is more flexible. Bytes can be store as `Vec<u8>`, and string slices ([`&str`](https://doc.rust-lang.org/std/primitive.str.html)) can be created with `str::from_utf8`. Unlike a `String` type, which has an owned UTF-8 buffer, `&str` is a borrowed UTF-8 view, it only stores the slice descriptor. That means if the RAM is large enough, after loading the whole text file into RAM, using string slices can be lightweight than copying bytes between buffers, while at the same time, it's able to be passed to regular expression engines.

[PyO3](../tools/pyo3.md) fills the gap between Python and Rust. It converts data types from Python, calls the native APIs, and converts data types from Rust back to Python.

So the Python layer and PyO3 layer are very thin, the heavy work is done in the Rust layer.

#### Key Data Types

There are a few aliases used to make the raw data type meaningful:

- `TokenBytes` (`Vec<u8>`): `u8`, an unsigned 8-bit integer, commonly written as `uint8`, `uint8_t` or `byte` in some other programming languages, is a primitive type in Rust. Vectors in Rust are resizable arrays.
- `TokenId` (`u16`): `u16`, similarly to `u8`, is another primitive type in Rust. It represents an unsigned 16-bit integer. The range of `u8` is `0~255`. The initial `vocab` contains these tokens. However when merging byte pairs, new token IDs will be created, they will be greater than `255`, so `u8` isn't enough to hold these values. Luckily, when training on TinyStories and OpenWebText, the maximum vocabulary size is 32k. The maximum number `u16` can hold is `0xFFFF` which is `65535` in decimal, is greater than 32k, so `u16` can be used to represent `TokenId`.
- `TokenIds` (`Vec<u16>`): After the pre-tokenization, the raw `TokenBytes` will be converted to `TokenIds` for training.
- `PackedPair` (`u32`): During the training, byte pairs, in fact pairs of token ids, will be counted, a `HashMap` will be used. We can use an array `[u16; 2]` or a tuple `(u16, u16)`, because the `std::collections::HashMap` accepts multiple types as keys in a hash map, as long as these types implement both the `Eq` and `Hash` traits. However these types are less efficient for hashing, and luckily, two 16-bit integers can be grouped as a 32-bit integer easily with bitwise operations, the same as unpacked from a 32-bit integer.

#### High-Level Overview

The Rust native code is designed and implemented with efficiency in mind.

##### Multi-threading

There are multiple steps during the whole process with similar situation: a group of data needs to be handled with the same process individually. This is very ideal for multi-threading. The main thread splits the group into non-overlapping chunks, each chunk is handled by a thread, each thread collects data, then the main thread merges these data.

> NOTE: Python also provides parallelism, in fact there are two concepts, multithreading vs multiprocessing. However due to the GIL (Global Interpreter Lock), standard CPython (before 3.14) limits CPU-bound multithreading (e.g. string processing), it's suitable for IO-related jobs. Multiprocessing suits this case, but it spawns new processes on the running system, and IPC (inter-process communication) is expensive. Keep this in mind if you are going to use parallelism in pure Python.

##### Regular Expression Engine

Regular expressions in this assignment are used for two situations:

- to split the text by special tokens which act as delimiters or hard boundaries.
- to pre-tokenize documents, see [gpt2-pretokenization-regex](../concepts/gpt2-pretokenization-regex.md).

The Python package `regex` isn't used because the whole process is designed in the pure Rust land, exchanging string between Rust and Python will be expensive, and lose the RAM efficient approach.

The widely used crate [`regex`](https://github.com/rust-lang/regex) isn't used as well, according to GPT and other language models (fact not checked yet), this crate does not support possessive quantifiers (e.g., `.*+` or `++`). Other Rust crates like [`fancy-regex`](https://github.com/fancy-regex/fancy-regex) and [`rust-onig`](https://github.com/rust-onig/rust-onig) may support that feature, however, I didn't choose these because I had not evaluated their compatibility, performance, and dependency tradeoffs yet.

[`libpcre2`](https://www.pcre.org) is chosen because:

1. It is a widely used, open-source C library that implements regular expression pattern matching using the same syntax and semantics as Perl 5
2. It is fundamental for powering regex capabilities in high-profile projects like Apache, PHP and Nmap. It can be installed via the system package manager on many Linux systems.
3. It supports **possessive quantifiers**.
4. It is possible to call C functions from Rust with [FFI](../concepts/ffi.md).

There is a wrapper [rust-pcre2](https://github.com/BurntSushi/rust-pcre2), but since there are not many APIs to be wrapped for this project, for educational purpose, a thin AI-made layer is used. Checkout [ffi.rs](https://github.com/IronBlood/cs336-rs/blob/main/src/ffi.rs).

##### The Flow

This section only talks the flow in the Rust layer, checkout [profile_bpe.rs](https://github.com/IronBlood/cs336-rs/blob/main/src/bin/profile_bpe.rs) to see the complete flow.

1. `find_chunk_boundaries` borrows the idea from `pretokenization_example.py`. The whole file content is read to RAM first, then this function finds boundaries similarly within every chunk of 4096 bytes.
2. `find_pretoken_spans` uses these boundaries to continue splitting the content in parallel by special tokens, returning vectors of `(usize, usize)` to represent the starting location (included) and the ending location (excluded) in the raw bytes of the content.
3. `build_token_freq_map` uses the GPT2 pretokenization regular expression to find what original tokens need to be trained and how many of each of the tokens.
4. `train_bpe` deals with byte pairs, merges and builds the vocabulary.

#### Validations and Optimizations

[verify.py](../../assignments/assignment1-basics/verify.py) is a naive implementation to validate the correctness of the Rust pretokenization. There is a binary in the Rust implementation which serialize the tokens (before training) and counts to a TSV format file, and this python script parses in an unoptimized approach, deserialize the TSV file, and compare the keys and counts. `TinyStoriesV2-GPT4-train.txt`, `TinyStoriesV2-GPT4-valid.txt` and `owt_valid.txt` have been used to validate, and all passed. `owt_train.txt` didn't finish because it used more than 32G of RAM, which led to a crash due to lack of RAM.

There are a few changes to improve the efficiency:

1. Enables JIT (just-in-time) for libpcre2. Before adopting JIT, it took more than 80min to pretokenize `owt_train.txt` on my 5800x desktop (even with multithreading enabled). With JIT, it only took about 100s (39s in `release` profile) to parse 6601892 unique tokens (2471753092 tokens in total).
2. Uses vectors of tuples of `(token, count)` instead of rebuilding hashmaps, because we already have unique tokens, no need to do extra hashing during each iteration of training.
3. Uses incremental pair counting by tracking the numbers of pairs to be removed and the numbers of pairs to be added, instead of counting every byte pair after a merge.
4. Uses `u32` to pack pairs of token ids for hashing.
5. Better hashmap operations, e.g. to remove an element immediately when its counting reaches 0, instead of filtering through all keys after all changes, to use one hashmap when possible, instead of merging multiple hashmaps.
6. Avoid using owned `Vec<u8>` as key of hashmaps, borrows `&[u8]` to reduce buffer copying.

### Problem train_bpe_tinystories

> (a) Train a byte-level BPE tokenizer on the TinyStories dataset, using a maximum vocabulary
> size of 10,000. Make sure to add the TinyStories <|endoftext|> special token to the vocabulary.
> Serialize the resulting vocabulary and merges to disk for further inspection. How much time
> and memory did training take? What is the longest token in the vocabulary? Does it make sense?

Resource usage was recorded with [GNU `time`](https://www.gnu.org/software/time/). The initial script didn't serialize the vocabulary and merges.

|                | Duration                | RAM      |
| :------------- | :---------------------- | :------- |
| Requirement    | <= 30 minutes (no GPUs) | <= 30 GB |
| Implementation | 8.88 seconds            | 2271 MB  |

The longest token (encoded) in the vocabulary is `Ġaccomplishment`.

**RAW DATA**:

```
Command being timed: "uv run -m cs336_basics.bpe data/TinyStoriesV2-GPT4-train.txt 10000"
User time (seconds): 71.26
System time (seconds): 4.14
Percent of CPU this job got: 848%
Elapsed (wall clock) time (h:mm:ss or m:ss): 0:08.88
Average shared text size (kbytes): 0
Average unshared data size (kbytes): 0
Average stack size (kbytes): 0
Average total size (kbytes): 0
Maximum resident set size (kbytes): 2271388
Average resident set size (kbytes): 0
Major (requiring I/O) page faults: 0
Minor (reclaiming a frame) page faults: 27759
Voluntary context switches: 38802
Involuntary context switches: 18204
Swaps: 0
File system inputs: 4351080
File system outputs: 0
Socket messages sent: 0
Socket messages received: 0
Signals delivered: 0
Page size (bytes): 4096
Exit status: 0
```

> (b) Profile your code. What part of the tokenizer training process takes the most time?

The profiling script is implemented in Rust [profile_bpe.rs](https://github.com/IronBlood/cs336-rs/blob/main/src/bin/profile_bpe.rs). To run this script, using:

```bash
cargo run --release --features profile-bpe --bin profile_bpe -- /path/to/TinyStoriesV2-GPT4-train.txt 10000
```

The argument `--release` is optional. With it, here is the time cost:

```
read file: 0.790s
find boundaries: 0.000s
find spans: 0.128s
span sort: 0.000s
flatten spans: 0.011s
build freq map: 4.221s
convert freq map: 0.005s
------
init pair counting: 0.001s
largest pair: 0.750s
replace: 3.052s
patch pair counting: 0.017s
------
train bpe: 3.829s
build vocab: 0.000s
```

Without it:

```
read file: 0.983s
find boundaries: 0.000s
find spans: 0.141s
span sort: 0.000s
flatten spans: 0.064s
build freq map: 18.376s
convert freq map: 0.033s
------
init pair counting: 0.014s
largest pair: 9.598s
replace: 11.562s
patch pair counting: 0.184s
------
train bpe: 21.389s
build vocab: 0.005s
```

Most of the time is spent on merging: 80% for the optimized version and 54% for the unoptimized version.

### Problem train_bpe_expts_owt

> (a) Train a byte-level BPE tokenizer on the OpenWebText dataset, using a maximum vocabulary
> size of 32,000. Serialize the resulting vocabulary and merges to disk for further inspection.
> What is the longest token in the vocabulary? Does it make sense?

Recorded with `time` as well (no serialization).

|                | Duration                | RAM       |
| :------------- | :---------------------- | :-------- |
| Requirement    | <= 12 hours (no GPUs)   | <= 100 GB |
| Implementation | 31 minutes              | 12.7 GB   |

The longest token (encoded) in the vocabulary is `ÃƃÃƂÃƃÃƂÃƃÃƂÃƃÃƂÃƃÃƂÃƃÃƂÃƃÃƂÃƃÃƂÃƃÃƂÃƃÃƂÃƃÃƂÃƃÃƂÃƃÃƂÃƃÃƂÃƃÃƂÃƃÃƂ`, decoded as `\xC3\x82\xC3\x83`, it doesn't make sense.

**RAW DATA**:

```
Command being timed: "uv run -m cs336_basics.bpe data/owt_train.txt 32000"
User time (seconds): 21973.87
System time (seconds): 50.95
Percent of CPU this job got: 1180%
Elapsed (wall clock) time (h:mm:ss or m:ss): 31:05.72
Average shared text size (kbytes): 0
Average unshared data size (kbytes): 0
Average stack size (kbytes): 0
Average total size (kbytes): 0
Maximum resident set size (kbytes): 12720444
Average resident set size (kbytes): 0
Major (requiring I/O) page faults: 35
Minor (reclaiming a frame) page faults: 2476424
Voluntary context switches: 144704
Involuntary context switches: 5160125
Swaps: 0
File system inputs: 21824440
File system outputs: 0
Socket messages sent: 0
Socket messages received: 0
Signals delivered: 0
Page size (bytes): 4096
Exit status: 0
```

> NOTE: for the task `train_bpe_expts_owt` or maybe even `train_bpe_tinystories`, my implementation loads the full text into the RAM because my desktop has 64GB RAM, this might not work on your system, especially the first one (12G). However it's possible to split the process into different isolated stages to avoid heavy RAM use:
>
> - Have a script to save the spans to a file.
> - Have a script which reads only one span into RAM, builds the freq map, and serialize to a file. This process can be executed in parallel.
> - Have another script to read each serialized freq map, deserialize and then merge into one final freq map. This is like the reducer.
> - Have the final script which loads the final freq map, then do BPE training.
>
> The serialized freq map for `owt_train.txt` might be just 100+ MB.

### Problem tokenizer

The implementation lives in the native implementation: [tokenizer.rs](https://github.com/IronBlood/cs336-rs/blob/main/src/tokenizer.rs). This note only records the Python-facing behavior and test status.

The PyO3 layer exposes a `Tokenizer` class which acts as the bridge between Python and the native implementation.

Local test changes in [test_tokenizer.py](../../assignments/assignment1-basics/tests/test_tokenizer.py):

- The three `.encode_iterable` tests are skipped because `.encode_iterable` is not implemented yet.
- `test_roundtrip_unicode_string_with_special_tokens` is skipped because per-token decoding is not fully supported yet. Some individual token IDs may decode to byte sequences that are not valid UTF-8 by themselves.
- The expectation of `test_overlapping_special_tokens` is changed to match the reference (OpenAI's `tiktoken`) behavior. The double special token is not preserved as one token.

### Problem tokenizer_experiments

The implementation lives in [tokenize_samples.rs](https://github.com/IronBlood/cs336-rs/blob/94a4c5c41583282328645445ec807f6c85ddc793/src/bin/tokenize_samples.rs). Usage:

```bash
cargo run --release --bin tokenize_samples /path/to/TinyStoriesV2-GPT4-valid.txt \
  --vocab /path/to/TinyStoriesV2-GPT4.vocab.txt \
  --merges /path/to/TinyStoriesV2-GPT4.merges.txt
```

> (a) Sample 10 documents from TinyStories and OpenWebText. Using your previously-trained
> TinyStories and OpenWebText tokenizers (10K and 32K vocabulary size, respectively),
> encode these sampled documents into integer IDs. What is each tokenizer’s compression ratio
> (bytes/token)?

Using the first 10 documents from the valid datasets of TinyStories and OpenWebText. The ratios are:

- TinyStories: 4.011 (4.059 with the first 100 documents)
- OpenWebText: 4.505 (4.445 with the first 100 documents)

> (b) What happens if you tokenize your OpenWebText sample with the TinyStories tokenizer?
> Compare the compression ratio and/or qualitatively describe what happens.

Switching tokenizers gives lower compression ratios:

- TinyStories documents encoded with OpenWebText tokenizer: 3.867
- OpenWebText documents encoded with TinyStories tokenizer: 3.405

Since a higher bytes/token ratio means better compression, both tokenizers become less efficient when used on data from the other distribution. The drop is larger for OpenWebText with the TinyStories tokenizer, which makes sense: TinyStories is simpler and narrower, while OpenWebText contains more diverse web text, punctuation, formatting, names, and unusual strings.

> (c) Estimate the throughput of your tokenizer (e.g., in bytes/second). How long would it take to
> tokenize the Pile dataset (825GB of text)?

With a single thread for encoding, the throughputs are:

- TinyStories: `16728673.580 bytes/s`
- OpenWebText: `14526728.345 bytes/s`

If the encoding runs at `14 MB/s`, it takes about **16** hours to encode the Pile dataset.

**NOTE**: I also tried two parallel encoding experiments, with and without caching. They are not faster for encoding, and even worse for TinyStories. Probably for a few reasons:

- Each document is not long enough, so it doesn't really help to split tokens and encode them in multiple threads.
- Pre-tokenized pieces are usually short enough, for example ` the`, ` a` and `.`. It takes extra time to build the cache and compute hashes for cache keys.

> (d) Using your TinyStories and OpenWebText tokenizers, encode the respective training and
> development datasets into a sequence of integer token IDs. We’ll use this later to train our
> language model. We recommend serializing the token IDs as a NumPy array of datatype
> `uint16`. Why is `uint16` an appropriate choice?

Because the vocabulary size is at most 32,000, so every token ID fits in 16 bits. `uint32` and `uint64` would also work, but they would use more memory without adding value for this vocabulary size. `uint16` works when the vocabulary size is `<= 65536`. For larger vocabularies, like `100k` or `200k`, `uint32` is needed.

## Chapter 3

In this section unit tests are split to different problems in different files, so `uv run pytest -k` is used.

[test_model.py](../../assignments/assignment1-basics/tests/test_model.py) contains:

- `test_linear`
- `test_embedding`
- `test_rmsnorm`
- `test_swiglu`
- `test_rope`
- `test_4d_scaled_dot_product_attention`
- `test_multihead_self_attention`
- `test_transformer_block`
- `test_transformer_lm`

[test_nn_utils.py](../../assignments/assignment1-basics/tests/test_nn_utils.py) contains:

- `test_softmax_matches_pytorch`

Implementation is stored in [nn.py](../../assignments/assignment1-basics/cs336_basics/nn.py) and [nn_utils.py](../../assignments/assignment1-basics/cs336_basics/nn_utils.py). Also see PyTorch explanations [torch.md](../tools/torch.md).

### Linear, Embedding, and RMSNorm

These three classes are the fundamental block, and they share the same pattern:

```py
class Foo(torch.nn.Module):
    def __init__(self, args):
        super().__init__()
        self.weight = torch.nn.Parameter(tensor)
```

### SwigLu

There are three linear layers, shown in the formula $\operatorname{FFN}(x) = W_2 \left(\operatorname{SiLU}(W_1 x) \odot W_3 x\right)$, and they are defined in the constructor, while the formula is implemented in `forward()`.

### RoPE

The key point is given a pair of `theta`, `d_k`, and `max_seq_len`, then the full rotation matrix is fixed. Inside the matrix, only two kinds of number is stored, given by a pair of `i` and `k`, which are `sin` and `cos`. So there are two tensors used to store the values, instead of the matrix, since most elements are just zeros.

These two tensors are passed to [`self.register_buffer()`](https://docs.pytorch.org/docs/2.14/generated/torch.nn.Module.html#torch.nn.Module.register_buffer), instead of `nn.Parameter()`, since they are like constants, not learned parameters, and can be restored easily.

The key part is to use `torch.arrange()` to create index related tensors for the later computation.

- `position = torch.arrange(max_seq_len)`
- `k = torch.arrange(d_k // 2)`

In the `forward()` function, the rotation block is restored by a given position, then merged with `torch.stack()`.

Currently to save a little bit space, a singleton pattern is used. See `get_rope(cfg, devide)`.

### Softmax

The helper function `softmax` in `nn_utils.py` basically implements the standard softmax, but in order to avoid `NaN` error, the formula is shifted a little bit with the following transformation:

$$
\begin{aligned}
\operatorname{softmax}(v)_i
&= \frac{\exp(v_i)}{\sum\nolimits_{j=1}^n \exp(v_j)} \\
&= \frac{\exp(v_i)/\exp(v_{max})}{\sum\nolimits_{j=1}^n \left(\exp(v_j)/\exp(v_{max})\right)} \\
&= \frac{\exp(v_i - v_{max})}{\sum\nolimits_{j=1}^n \exp(v_j - v_{max})}
\end{aligned}
$$

### Scaled Dot-product Attention

This is another helper function. The implementation is also pretty straightforward. The key API used is [`torch.Tensor.masked_fill`](https://docs.pytorch.org/docs/2.14/generated/torch.Tensor.masked_fill.html), which returns a new tensor, according to the binary matrix `mask`, if exist, if an element in `mask` is true, then the value in the original matrix is copied, otherwise the new value is set to negative infinite.

> [!NOTE]
> There is another in-place API which is `torch.Tensor.masked_fill_()`.

### Multi-Head Self-Attention

There are two test cases associated with `uv run pytest -k test_multihead_self_attention`, one without RoPE while the other one with RoPE.

The prototypes of the constructor and `forward` of `MultiheadSelfAttention` were not given in the assignment, so they are inferred from the adapters.

In the Equation 14, there are four linear layers. These layers are named based on the adapters, for example in `run_transformer_block`, so that `.load_state_dict()` can be used instead of assigning to `.weight.data` one by one. That is why `output_proj` is named instead of `o_proj`.

In the `forward()` function, the combination of `torch.tril()` and `torch.ones()` creates a lower triangle matrix filled by `1`s. `Q`, `K`, and `V` first get computed, then rearranged for `scaled_dot_product_attention()`. The output is rearranged before passing to `.output_proj()`.

### Transformer Block

The layers are also named after the usage in the test cases. The key in `forward` is the use of `torch.arange()` to create `token_positions`, which is used by RoPE.

### Transformer LM

[`torch.nn.ModuleList()`](https://docs.pytorch.org/docs/2.14/generated/torch.nn.ModuleList.html) creates an object to hold modules like a regular Python list. In this case, it holds `num_layers` of `TransformerBlock`s.

### ReProblem 3a

> Consider a GPT-2 XL-sized model using our assignment architecture, which has the following configuration:
>
> - vocab_size: 50,257
> - context_length: 1,024
> - num_layers: 48
> - d_model: 1,600
> - num_heads: 25
> - d_ff: 4,288 (the nearest multiple of 64 to 8 / 3 × 1,600)
>
> Suppose we constructed our model using this configuration. How many trainable parameters would our model have? Assuming each parameter is represented using single-precision floating point, how much memory is required to just load this model?

Let's break it down.

1. The `token_embeddings` layer has $\mathrm{vocab_size} \times \mathrm{d_model} = 80,411,200$ parameters.
2. The `ln_final` layer has 1,600 parameters.
3. The `lm_head` layer has $\mathrm{d_model} \times \mathrm{vocab_size} = 80,411,200$ parameters.

Now let's dig into a single `TransformerBlock`.

1. `ln` has 1,600 parameters.
2. `ln2` has 1,600 parameters.
3. `ffn` has $3 \times \mathrm{d_model} \times \mathrm{d_ff} = 3 \times 1600 \times 4288 = 20,582,400$ parameters.
4. `attn` has $4 \times \mathrm{d_model} \times \mathrm{d_model} = 4 \times 1600 \times 1600 = 10,240,000$ parameters.

So a single `TransformerBlock` layer has $1600 \times 2 + 20582400 + 10240000 = 30,825,600$ parameters.

Thus the number of total trainable parameters is:

$$
80411200 \times 2 + 1600 + 30825600 \times 48 = 1,640,452,800 \approx 1.5B
$$

This model requires 6.56 GB memory approximately.

### Problem 3b

> Identify the matrix multiplies required to complete a forward pass of our GPT-2 XL-shaped model. How many FLOPs do these matrix multiplies require in total? Assume that our input sequence has `context_length` tokens.

`.token_embeddings()` looks up from the embedding table, no computation involved. The returned matrix $\in \mathbb{R}^{\mathrm{context_length} \times \mathrm{d_model}}$.

| Module | Shapes | FLOPs |
| :----: | :----: | :---: |
| `Linear` | $x \in \mathbb{R}^{m \times n}$, $W \in \mathbb{R}^{n \times p}$ | $2mnp$ |
| `SwigLU` | $x \in \mathbb{R}^{\mathrm{seq} \times d_{\mathrm{model}}}$ | $6\mathrm{seq}d_{\mathrm{model}}d_{\mathrm{ff}}$ |
| `MultiheadSelfAttention` | $x \in \mathbb{R}^{\mathrm{seq} \times d_{\mathrm{model}}}$ | $8\mathrm{seq}d_{\mathrm{model}}^2 + 4\mathrm{seq}^2d_{\mathrm{model}}$ |
| `TransformerBlock` | $x \in \mathbb{R}^{\mathrm{seq} \times d_{\mathrm{model}}}$ | `attn` + `ffn` |
| `lm_head` | $x \in \mathbb{R}^{\mathrm{seq} \times d_{\mathrm{model}}}$ | $2 \mathrm{seq} \times d_{\mathrm{model}} \times \mathrm{vocab}$ |

Notes:

- `SwigLU`:
  - `.w1()` and `.w3()` take $2 \times 2 \mathrm{seq} d_{\mathrm{model}}d_{\mathrm{ff}}$ FLOPs in total.
  - The final `.w2()` takes $2 \mathrm{seq} d_{\mathrm{model}}d_{\mathrm{ff}}$ FLOPs.
- `MultiheadSelfAttention`:
  - Q, K, and V take $3 \times 2 \mathrm{seq} d_{\mathrm{model}}^2$ FLOPs.
  - In `scaled_dot_product_attention`:
    - The `einsum` of `score` takes $\mathrm{heads} \times 2\mathrm{seq}^2d_k = 2\mathrm{seq}^2d_{\mathrm{model}}$ FLOPs.
    - The final `einsum` takes $2 \mathrm{seq}^2 d_{\mathrm{model}}$ FLOPs.
  - The final output projection takes $2 \mathrm{seq} d_{\mathrm{model}}^2$ FLOPs.
- `TransformerBlock`:
  - Pre-norm layers do not contribute matrix multiplies.
  - So the FLOPs of a single `TransformerBlock` is the sum of `attn` and `ffn`.

Thus, the total FLOPs required:

$$
\begin{aligned}
\mathrm{total} &= \mathrm{layers} \times (\mathrm{attn} + \mathrm{ffn}) + \mathrm{lm\_head} \\
&= 48 \times (8 \times 1024 \times 1600^2 + 4 \times 1024^2 \times 1600 + 6 \times 1024 \times 1600 \times 4288) + 2 \times 1024 \times 1600 \times 50257 \\
&= 48 \times (20,971,520,000 + 6,710,886,400 + 42,152,755,200) + 164,682,137,600 \\
&= 3,516,769,894,400 \approx 3.52 \times 10^{12}
\end{aligned}
$$

### Problem 3c

> Based on your analysis above, which parts of the model require the most FLOPs?

The FFN is the largest per Transformer block. Within attention, the Q/K/V/output projections cost more than the attention score/value mixing at context length 1024. The `lm_head` is also expensive because it projects every position from `d_model` to the full vocabulary, but it happens only once, while attention and FFN happen once per Transformer block.

### Problem 3d

> Repeat your analysis with GPT-2 small (12 layers, 768 d_model, 12 heads), GPT-2 medium (24 layers, 1024 d_model, 16 heads), and GPT-2 large (36 layers, 1280 d_model, 20 heads). As the model size increases, which parts of the Transformer LM take up proportionally more or less of the total FLOPs?

Let's fix `context_length` to `1024`.

|     | Formula | GPT-2 small | GPT-2 medium | GPT-2 large | GPT-2 XL
| :-- | :------ | :--: | :--: | :--: | :--: |
| `d_ff` | $\frac{8}{3} \mathrm{d\_model}$ | 2048 | 2752 | 3392 | 4288 |
| Attention projection | $8 \mathrm{seq} d_{\mathrm{model}}^2$ | 4.5Gi | 8Gi | 12.5Gi | 19.53Gi |
| Attention score | $4 \mathrm{seq}^2 d_{\mathrm{model}}$ | 3Gi | 4Gi | 5Gi | 6.25Gi |
| FFN | $6 \mathrm{seq} d_{\mathrm{model}} d_{\mathrm{ff}}$ | 9Gi | 16.13Gi | 24.84Gi | 39.26Gi |
| lm_head | $2 \mathrm{seq} d_{\mathrm{model}} \mathrm{vocab}$ | 73.62Gi | 98.16Gi | 122.70Gi | 153.37Gi |
| total | $\mathrm{layers} \times (\mathrm{attn\_proj} + \mathrm{attn\_score} + \mathrm{ffn}) + \mathrm{lm\_head}$ | 271.62Gi | 773.16Gi | 1647.07Gi | 3275.25Gi |

As the model size increases, `lm_head` takes less of the total FLOPs, while attention projection and FFN increase significantly.

### Problem 3e

> Take GPT-2 XL and increase the context length to 16,384. How does the total FLOPs for one forward pass change? How does the relative contribution of FLOPs of the model components change?

| Context Length | 1024 | 16,384 |
| :------------- | ---: | -----: |
| Attention projection | 19.53Gi | 312.5Gi |
| Attention score | 6.25Gi | 1600Gi |
| FFN | 39.26Gi | 628.13Gi |
| lm_head | 153.37Gi | 2453.96Gi |
| total | 3275.25Gi | 124403.96Gi |

Increasing context length from 1,024 to 16,384 makes the sequence 16x longer. Attention projection, FFN and lm_head term scale linearly with sequence length, so they grow by 16x. The attention score/value mixing term scales quadratically with sequence length, so it grows by 256x.

As a result, the attention score/value term becomes much more important. At context length 1,024, FFN is the largest per-block cost. At context length 16,384, the quadratic attention term dominates the per-block FLOPs.
