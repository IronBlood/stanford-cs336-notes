#[pyo3::pymodule]
mod cs336_basics {
    use std::{collections::HashMap, fs, path::PathBuf, thread};

    use cs336_rs::{
        file::{write_merges, write_vocab},
        utils::{
            BpeTrainingResult, build_token_freq_map, convert_freq_map_to_u16,
            find_chunk_boundaries, find_pretoken_spans, train_bpe,
        },
    };
    use pyo3::prelude::*;

    type BpeTrainingResultVocab = HashMap<usize, Vec<u8>>;
    type BpeTrainingResultMerges = Vec<(Vec<u8>, Vec<u8>)>;
    type PyBpeTrainingResult = (BpeTrainingResultVocab, BpeTrainingResultMerges);

    fn bpe_internal(
        input_path: &PathBuf,
        vocab_size: u16,
        special_tokens: &[String],
    ) -> BpeTrainingResult {
        let content = fs::read(&input_path).expect("file should be readable");
        let cpus = thread::available_parallelism()
            .map(|count| count.get())
            .unwrap_or(1);

        let boundaries = find_chunk_boundaries(&content, cpus, &special_tokens);
        let mut spans =
            find_pretoken_spans(&content, &boundaries, &special_tokens).expect("should succeed");
        spans.sort();

        let gpt2_regex_str =
            r"'(?:[sdmt]|ll|ve|re)| ?\p{L}++| ?\p{N}++| ?[^\s\p{L}\p{N}]++|\s++$|\s+(?!\S)|\s";

        let all_pieces: Vec<_> = spans.into_iter().flatten().collect();
        let freq_map = build_token_freq_map(&content, &all_pieces, cpus, &gpt2_regex_str)
            .expect("should succeed");

        let freq_map = convert_freq_map_to_u16(freq_map);
        let result = train_bpe(freq_map, vocab_size as usize, &special_tokens, cpus)
            .expect("should succeed");

        result
    }

    #[pyfunction]
    /// This API is purely for the assignment `train_bpe`, the test cases require special_tokens
    /// to be inserted in the vocabulary.
    fn bpe_with_special_token_merged(
        input_path: PathBuf,
        vocab_size: u16,
        special_tokens: Vec<String>,
    ) -> PyBpeTrainingResult {
        let result = bpe_internal(&input_path, vocab_size, &special_tokens);
        let mut vocab: BpeTrainingResultVocab = HashMap::new();
        vocab.insert(0, special_tokens[0].clone().into());
        for (id, bytes) in result.vocab.into_iter().enumerate() {
            vocab.insert(id + 1, bytes);
        }
        (vocab, result.merges)
    }

    #[pyfunction]
    /// This API is the actual one which will be mainly used with custom defined formats
    /// of vocabs and merges. The format might be changed in the future.
    fn bpe(
        input_path: PathBuf,
        vocab_size: u16,
        special_tokens: Vec<String>,
        vocab_path: PathBuf,
        merges_path: PathBuf,
    ) {
        let result = bpe_internal(&input_path, vocab_size, &special_tokens);
        write_vocab(&vocab_path, &result.vocab);
        write_merges(&merges_path, &result.merges);
    }
}
