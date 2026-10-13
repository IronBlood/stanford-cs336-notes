# Lecture 11: Scaling Laws

## Keywords

- Hyperparameter transfer
- Warmup-stable-decay schedules
- Maximal update parameterization (muP)
- Optimizer scaling
- Muon

## Summary

The lecture examines how scaling studies guide real model development, using reports such as MiniCPM and DeepSeek. Two approaches address sensitive hyperparameters: reparameterize the model to preserve useful behavior across widths, or fit scaling relationships for optimal learning rates and batch sizes. Warmup-stable-decay schedules make training horizons easier to extend and compare. Optimizer comparisons introduce Muon's treatment of matrix updates and stress that apparent gains depend on scale, training duration, and tuning fairness. A derivation of maximal update parameterization starts from invariants on activation magnitudes and feature updates. These methods improve predictability, but transferring settings still requires checking assumptions and experimental regimes.

Source: [YouTube transcript](../../raw/transcripts/Stanford%20CS336%20Language%20Modeling%20from%20Scratch%20%EF%BD%9C%20Spring%202026%20%EF%BD%9C%20Lecture%2011%EF%BC%9A%20%20Scaling%20Laws-vTfEyOyzV9E.en-US.srt).

