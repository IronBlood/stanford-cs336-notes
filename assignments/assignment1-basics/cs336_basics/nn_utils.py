from typing import Optional
import torch
from jaxtyping import Bool, Float
from einops import einsum

def softmax(x: torch.Tensor, dim: int) -> torch.Tensor:
    x_max = x.max(dim=dim, keepdim=True).values
    shifted = x - x_max
    e = torch.exp(shifted)
    sum = e.sum(dim=dim, keepdim=True)
    return e / sum

def scaled_dot_product_attention(
    Q: Float[torch.Tensor, " ... queries d_k"],
    K: Float[torch.Tensor, " ... keys d_k"],
    V: Float[torch.Tensor, " ... keys d_v"],
    mask: Optional[Bool[torch.Tensor, " ... queries keys"]] = None,
) -> Float[torch.Tensor,  " ... queries d_v"]:
    d_k = K.shape[-1]
    score: Float[torch.Tensor, "... queries keys"] = einsum(Q, K, "... queries d_k, ... keys d_k -> ... queries keys") / (d_k ** 0.5) # the same as `mask`
    if mask is not None:
        score = score.masked_fill(~mask, float("-inf"))

    weight = softmax(score, -1)

    return einsum(weight, V, "... queries keys, ... keys d_v -> ... queries d_v")
