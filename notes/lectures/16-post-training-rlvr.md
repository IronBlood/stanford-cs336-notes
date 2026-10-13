# Lecture 16: Post-Training - RLVR

## Keywords

- Verifiable rewards
- Policy gradients
- Group relative policy optimization (GRPO)
- Reward and length biases
- Rollout infrastructure

## Summary

The lecture contrasts preference-based reward models with verifiable feedback from domains such as mathematics and coding. It reviews PPO's practical complexity, then explains GRPO's use of groups of sampled responses to estimate advantages without a separate value model. Examining normalization choices reveals possible biases in difficulty weighting and response length. DeepSeek, Kimi, and Qwen examples show how reasoning demonstrations, reward design, curricula, and distillation fit into larger training pipelines. Rollout generation introduces systems challenges involving long responses, weight transfer, utilization, and off-policy reuse. Verifiable rewards support further optimization, but imperfect graders and environments can still be exploited, so reward validity needs close attention.

Source: [YouTube transcript](../../raw/transcripts/Stanford%20CS336%20Language%20Modeling%20from%20Scratch%20%EF%BD%9C%20Spring%202026%20%EF%BD%9C%20Lecture%2016%EF%BC%9A%20Post-Training%20-%20RLVR-dIFAi87Ws4E.en-US.srt).

