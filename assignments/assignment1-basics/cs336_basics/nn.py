import torch
from jaxtyping import Bool, Float, Int
from typing import Optional
from einops import rearrange

from . import nn_utils

class Linear(torch.nn.Module):
    def __init__(
        self,
        in_features: int,
        out_features: int,
        device: Optional[torch.device] = None,
        dtype: Optional[torch.dtype] = None,
    ):
        """
        Args:
            in_features: final dimension of the input
            out_features: final dimension of the output
        """
        self.in_features = in_features
        self.out_features = out_features
        sigma = (2.0 / (in_features + out_features)) ** 0.5

        super().__init__()
        self.weight = torch.nn.Parameter(torch.empty(
            out_features,
            in_features,
            device=device,
            dtype=dtype,
        ))
        torch.nn.init.trunc_normal_(
            self.weight,
            std=sigma,
            a=-3 * sigma,
            b=3*sigma
        )

    def forward(
        self,
        x: Float[torch.Tensor, " ... d_in"],
    ) -> Float[torch.Tensor, " ... d_out"]:
        return x @ self.weight.T

class Embedding(torch.nn.Module):
    def __init__(
        self,
        num_embeddings: int,
        embedding_dim: int,
        device: Optional[torch.device] = None,
        dtype: Optional[torch.dtype] = None,
    ):
        """
        Args:
            num_embeddings: Size of the vocabulary
            embedding_dim: Dimension of the embedding vectors
        """
        sigma = 1

        super().__init__()
        self.weight = torch.nn.Parameter(torch.empty(
            num_embeddings,
            embedding_dim,
            device=device,
            dtype=dtype
        ))
        torch.nn.init.trunc_normal_(
            self.weight,
            std=sigma,
            a=-3 * sigma,
            b=3*sigma
        )

    def forward(
        self,
        token_ids: Int[torch.Tensor, "..."],
    ) -> torch.Tensor:
        """Lookup the embedding vectors for the given token IDs.
        """
        return self.weight[token_ids]

class RMSNorm(torch.nn.Module):
    def __init__(
        self,
        d_model: int,
        eps: float = 1e-5,
        device=None,
        dtype=None,
    ):
        self.shape = d_model
        self.eps = eps
        super().__init__()
        self.weight = torch.nn.Parameter(
            torch.ones(
                self.shape,
                device=device,
                dtype=dtype
            )
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        in_type = x.dtype
        x = x.to(torch.float32)
        rms = torch.sqrt(torch.mean(x ** 2, dim=-1, keepdim=True) + self.eps)
        normalized = x / rms
        result = normalized * self.weight
        return result.to(in_type)

class SwigLU(torch.nn.Module):
    def __init__(
        self,
        d_model: int,
        d_ff: int,
        device=None,
        dtype=None,
    ):
        self.d_model = d_model
        self.d_ff = d_ff
        factory_kwargs = {
            "device": device,
            "dtype": dtype,
        }

        super().__init__()

        self.w1 = Linear(d_model, d_ff, **factory_kwargs)
        self.w3 = Linear(d_model, d_ff, **factory_kwargs)
        self.w2 = Linear(d_ff, d_model, **factory_kwargs)

    def forward(self, x: torch.Tensor):
        w1_x = self.w1(x)
        w3_x = self.w3(x)
        silu_w1_x = w1_x * torch.sigmoid(w1_x)
        return self.w2(silu_w1_x * w3_x)

class RotaryPositionalEmbedding(torch.nn.Module):
    sin: torch.Tensor
    cos: torch.Tensor

    def __init__(
        self,
        theta: float,
        d_k: int,
        max_seq_len: int,
        device=None,
    ):
        super().__init__()

        self.theta = theta
        self.d_k = d_k
        self.max_seq_len = max_seq_len

        # shape (max_seq_len, 1)
        positions = torch.arange(max_seq_len, device=device)[:, None]

        if d_k % 2 != 0:
            raise ValueError("d_k is expected to be an even number")

        # shape (d_k / 2, )
        k = torch.arange(d_k // 2, device=device)
        freq = 1.0 / (theta ** (2 * k / d_k))

        # shape (max_seq_len, d_k / 2)
        angles = positions * freq

        cos = torch.cos(angles)
        sin = torch.sin(angles)

        self.register_buffer("cos", cos, persistent=False)
        self.register_buffer("sin", sin, persistent=False)

    def forward(self, x: torch.Tensor, token_positions: torch.Tensor) -> torch.Tensor:
        cos = self.cos[token_positions] # (..., seq_len, d_k / 2)
        sin = self.sin[token_positions] # (..., seq_len, d_k / 2)

        x_even = x[..., 0::2]
        x_odd  = x[..., 1::2]

        rotated_even = x_even * cos - x_odd * sin
        rotated_odd  = x_even * sin + x_odd * cos
        return torch.stack((rotated_even, rotated_odd), dim=-1).flatten(-2)

class RopeCfg:
    def __init__(
        self,
        d_k: int,
        theta: float,
        max_seq_len: int,
    ):
        self.d_k = d_k
        self.theta = theta
        self.max_seq_len = max_seq_len

rope_cache = {}
def get_rope(
    cfg: RopeCfg,
    device: Optional[torch.device],
) -> RotaryPositionalEmbedding:
    key = (cfg.d_k, cfg.theta, cfg.max_seq_len, device)
    if key not in rope_cache:
        rope_cache[key] = RotaryPositionalEmbedding(cfg.theta, cfg.d_k, cfg.max_seq_len, device=device)
    return rope_cache[key]

class MultiheadSelfAttention(torch.nn.Module):
    rope_cfg: Optional[RopeCfg]

    def __init__(
        self,
        d_model: int,
        num_heads: int,
        max_seq_len: Optional[int] = None,
        theta: Optional[float] = None,
        device: Optional[torch.device] = None,
        dtype: Optional[torch.dtype] = None,
    ):
        """
        Args:
            d_model: Dimensionality of the Transformer block inputs.
            num_heads: Number of heads to use in multi-head self-attention.
        """
        factory_kwargs = {
            "device": device,
            "dtype": dtype,
        }

        super().__init__()

        self.d_model = d_model
        self.num_heads = num_heads

        # TODO: d_model % num_heads should be zero
        self.d_k = d_model // num_heads
        self.d_v = self.d_k
        if theta is not None and max_seq_len is not None:
            self.rope_cfg = RopeCfg(self.d_k, theta, max_seq_len)
        else:
            self.rope_cfg = None

        # (d_model, d_model)
        self.q_proj = Linear(d_model, d_model, **factory_kwargs)
        self.k_proj = Linear(d_model, d_model, **factory_kwargs)
        self.v_proj = Linear(d_model, d_model, **factory_kwargs)
        self.output_proj = Linear(d_model, d_model, **factory_kwargs)

    def forward(
        self,
        x: Float[torch.Tensor, " ... sequence_length d_model"],
        token_positions: Optional[Int[torch.Tensor, " ... sequence_length"]] = None,
    ) -> Float[torch.Tensor, " ... sequence_length d_model"]:
        # (... sequence_length d_model)
        Q: torch.Tensor = self.q_proj(x)
        K: torch.Tensor = self.k_proj(x)
        V: torch.Tensor = self.v_proj(x)

        Q = rearrange(
            Q,
            "... seq (heads d_k) -> ... heads seq d_k",
            heads=self.num_heads,
        )
        K = rearrange(
            K,
            "... seq (heads d_k) -> ... heads seq d_k",
            heads=self.num_heads,
        )
        if self.rope_cfg is not None and token_positions is not None:
            rope = get_rope(self.rope_cfg, device=token_positions.device)
            Q = rope(Q, token_positions)
            K = rope(K, token_positions)
        V = rearrange(
            V,
            "... seq (heads d_v) -> ... heads seq d_v",
            heads=self.num_heads,
        )

        # TODO: suggested by ChatGPT
        seq_len = x.shape[-2]
        mask = torch.tril(
            torch.ones(seq_len, seq_len, device=x.device, dtype=torch.bool)
        )
        out = nn_utils.scaled_dot_product_attention(Q, K, V, mask)

        out = rearrange(out, "... heads seq d_v -> ... seq (heads d_v)")

        return self.output_proj(out)

class TransformerBlock(torch.nn.Module):
    rope_cfg: Optional[RopeCfg]

    def __init__(
        self,
        d_model: int,
        num_heads: int,
        d_ff: int,
        max_seq_len: Optional[int] = None,
        theta: Optional[float] = None,
        device: Optional[torch.device] = None,
        dtype: Optional[torch.dtype] = None,
    ):
        super().__init__()

        self.d_model = d_model
        self.num_heads = num_heads
        self.d_ff = d_ff

        if max_seq_len is not None and theta is not None:
            self.rope_cfg = RopeCfg(d_model // num_heads, theta, max_seq_len)
        else:
            self.rope_cfg = None

        factory_kwargs = {
            "device": device,
            "dtype": dtype,
        }
        self.ln1 = RMSNorm(d_model, **factory_kwargs)
        self.attn = MultiheadSelfAttention(
            d_model,
            num_heads,
            max_seq_len,
            theta,
            **factory_kwargs
        )
        self.ln2 = RMSNorm(d_model, **factory_kwargs)
        self.ffn = SwigLU(d_model, d_ff, **factory_kwargs)

    def forward(self, x: torch.Tensor):
        seq_len = x.shape[-2]
        token_positions = torch.arange(seq_len, device=x.device) # ChatGPT
        # TODO: inplace?
        y = x + self.attn(self.ln1(x), token_positions)
        return y + self.ffn(self.ln2(y))

class TransformerLM(torch.nn.Module):
    def __init__(
        self,
        vocab_size: int,
        context_length: int,
        d_model: int,
        num_layers: int,
        num_heads: int,
        d_ff: int,
        rope_theta: float,
        device: Optional[torch.device] = None,
        dtype: Optional[torch.dtype] = None,
    ):
        factory_kwargs = {
            "device": device,
            "dtype": dtype,
        }

        super().__init__()

        self.token_embeddings = Embedding(vocab_size, d_model, **factory_kwargs)

        self.layers = torch.nn.ModuleList([
            TransformerBlock(
                d_model,
                num_heads,
                d_ff,
                context_length,
                rope_theta,
                **factory_kwargs,
            )
            for _ in range(num_layers)
        ])

        self.ln_final = RMSNorm(d_model, **factory_kwargs)

        # TODO: double check
        self.lm_head = Linear(d_model, vocab_size, **factory_kwargs)

    def forward(
        self,
        input_ids: Int[torch.Tensor, "batch_size sequence_length"],
        #token_positions: Optional[torch.Tensor] = None,
    ):
        x = self.token_embeddings(input_ids)
        for layer in self.layers:
            x = layer(x)

        x = self.ln_final(x)

        x = self.lm_head(x)

        return x
