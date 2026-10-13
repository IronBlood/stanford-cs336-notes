# Lecture 14: Data

## Keywords

- Text extraction
- Quality filtering
- MinHash and locality-sensitive hashing
- Data mixture optimization
- Synthetic post-training data

## Summary

The lecture examines the pipeline from raw documents to training mixtures. HTML and PDF extraction must recover useful content without losing important structure. Filtering defines a target distribution and uses rules or lightweight classifiers to select relevant data; suitable thresholds depend on training scale and available diversity. Exact and approximate deduplication reduce redundant training, with Jaccard similarity, MinHash, and locality-sensitive hashing providing scalable tools. Mixture optimization uses proxy models to choose source weights, but must account for repetition, scarcity, and downstream overfitting. The final section covers synthetic post-training data, including teacher-generated reasoning responses and coding trajectories whose environments can be difficult to construct.

Source: [YouTube transcript](../../raw/transcripts/Stanford%20CS336%20Language%20Modeling%20from%20Scratch%20%EF%BD%9C%20Spring%202026%20%EF%BD%9C%20Lecture%2014%EF%BC%9A%20Data-5sxHosTLPF8.en-US.srt).

