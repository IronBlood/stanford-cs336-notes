# Lecture 3: Architectures

## Keywords

- Normalization
- Gated activations
- Rotary position embeddings (RoPE)
- Training stability
- Grouped-query attention (GQA)

## Summary

The lecture surveys modern transformer architectures to distinguish common defaults from choices that remain unsettled. It explains why normalization usually sits outside the residual stream, why RMSNorm and gated feed-forward activations are popular, and how rotary embeddings encode relative position. Architectural hyperparameters are considered alongside practical training concerns rather than as isolated design choices. Stability techniques include controlling logits, normalizing queries and keys, and regularizing the output softmax. The final discussion connects architecture to inference: grouped-query attention reduces KV-cache costs, while alternating local and global attention helps manage long contexts. The central theme is balancing expressiveness, numerical stability, and hardware efficiency.

Source: [YouTube transcript](../../raw/transcripts/Stanford%20CS336%20Language%20Modeling%20from%20Scratch%20%EF%BD%9C%20Spring%202026%20%EF%BD%9C%20Lecture%203%EF%BC%9A%20Architectures-lVynu4bo1rY.en-US.srt).

