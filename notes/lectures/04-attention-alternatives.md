# Lecture 4: Attention Alternatives

## Keywords

- Linear attention
- State-space models
- Hybrid architectures
- Mixture of experts (MoE)
- Load balancing

## Summary

The lecture develops attention alternatives by rearranging matrix multiplication to obtain linear attention and an equivalent recurrent state update. Input-dependent gates and more selective updates lead to models such as Mamba-2 and gated DeltaNet. Combining these layers with full attention provides a practical tradeoff between long-context efficiency and expressiveness; sparse attention offers another route. The second half introduces mixtures of experts, which increase total parameters without activating every parameter for each token. It examines routing, expert collapse, load balancing, communication, and stability. DeepSeek examples illustrate how attention compression and expert design interact with the hardware and distributed execution strategy.

Source: [YouTube transcript](../../raw/transcripts/Stanford%20CS336%20Language%20Modeling%20from%20Scratch%20%EF%BD%9C%20Spring%202026%20%EF%BD%9C%20Lecture%204%EF%BC%9A%20Attention%20Alternatives-cKSwj_qZ8Jg.en-US.srt).

