#[pyo3::pymodule]
mod cs336_basics {
    use std::{collections::HashMap, fs, path::PathBuf, thread};

    use cs336_rs::utils::{
        Span, build_token_freq_map, convert_freq_map_to_u16, find_chunk_boundaries,
        find_pretoken_spans, train_bpe,
    };
    use pyo3::prelude::*;

    type BpeTrainingResultVocab = HashMap<usize, Vec<u8>>;
    type BpeTrainingResultMerges = Vec<(Vec<u8>, Vec<u8>)>;
    type PyBpeTrainingResult = (BpeTrainingResultVocab, BpeTrainingResultMerges);

    #[pyfunction]
    fn bpe(
        input_path: PathBuf,
        vocab_size: u16,
        special_tokens: Vec<String>,
    ) -> PyBpeTrainingResult {
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

        let all_pieces: Vec<Span> = spans.into_iter().flatten().collect();
        let freq_map = build_token_freq_map(&content, &all_pieces, cpus, &gpt2_regex_str)
            .expect("should succeed");

        let freq_map = convert_freq_map_to_u16(freq_map);
        let result = train_bpe(freq_map, vocab_size as usize, &special_tokens, cpus)
            .expect("should succeed");
        let mut vocab: BpeTrainingResultVocab = HashMap::new();
        vocab.insert(0, special_tokens[0].clone().into());
        for (id, bytes) in result.vocab.into_iter().enumerate() {
            vocab.insert(id + 1, bytes);
        }
        (vocab, result.merges)
    }
}
