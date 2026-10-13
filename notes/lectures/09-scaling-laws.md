# Lecture 9: Scaling Laws

## Keywords

- Power-law scaling
- Compute-optimal training
- IsoFLOP experiments
- Critical batch size
- Kaplan and Chinchilla

## Summary

The lecture presents scaling laws as empirical tools for predicting model performance and making decisions before an expensive training run. It connects power-law learning curves to classical statistical estimation, then examines scaling with data, parameters, compute, architecture, and hyperparameters. Data quality, repetition, and mixture choices can change the usefulness of additional tokens. Critical batch size describes diminishing returns from increasing batches, while learning-rate behavior also changes with scale. The Kaplan and Chinchilla studies illustrate how to allocate compute between model size and training data. Their disagreement emphasizes careful parameter accounting, training schedules, and experimental design, with IsoFLOP sweeps offering a useful comparison method.

Source: [YouTube transcript](../../raw/transcripts/Stanford%20CS336%20Language%20Modeling%20from%20Scratch%20%EF%BD%9C%20Spring%202026%20%EF%BD%9C%20Lecture%209%EF%BC%9A%20Scaling%20Laws-Q15rhEWZPQ4.en-US.srt).

