import torch
import math
from collections.abc import Callable, Iterable
from typing import Any, Optional, TypeAlias, cast
from jaxtyping import Float, Int

def cross_entropy(
    logits: Float[torch.Tensor, " batch_size vocab_size"],
    targets: Int[torch.Tensor, " batch_size"],
) -> Float[torch.Tensor, ""]:
    batch_size = logits.shape[0]
    max_logits = logits.max(dim=-1).values
    # [:, None] is important
    log_sum_exp = torch.log(torch.exp(logits - max_logits[:, None]).sum(dim=-1))
    target_logits = logits[torch.arange(batch_size, device=logits.device), targets]
    losses = max_logits + log_sum_exp - target_logits
    return torch.mean(losses)

ParamsT: TypeAlias = (
    Iterable[torch.Tensor]
    | Iterable[dict[str, Any]]
    | Iterable[tuple[str, torch.Tensor]]
)

class AdamW(torch.optim.Optimizer):
    def __init__(
        self,
        params: ParamsT,
        lr: float = 1e-3,
        betas: tuple[float, float] = (0.9, 0.999),
        eps: float = 1e-8,
        weight_decay: float = 1e-2,
    ):
        if lr < 0:
            raise ValueError(f"Invalid learning rate: {lr}")
        defaults = {
            "lr": lr,
            "betas": betas,
            "eps": eps,
            "weight_decay": weight_decay,
        }
        super().__init__(params, defaults)

    def step(self, closure: Optional[Callable] = None):
        # loss = None if closure is None else closure()
        loss = None
        if closure is not None:
            # TODO used in PyTorch
            with torch.enable_grad():
                loss = closure()
        beta1: float
        beta2: float

        for group in self.param_groups:
            # for type inference
            params = cast(Iterable[torch.Tensor], group["params"])

            lr: float = group["lr"]
            beta1, beta2 = group["betas"]
            eps: float = group["eps"]
            weight_decay: float = group["weight_decay"]

            # NOTE: precompute
            weight_decay_scale = lr * weight_decay
            one_minus_beta1 = 1 - beta1
            one_minus_beta2 = 1 - beta2

            # each `p` is one trainable parameter tensor
            for p in params:
                if p.grad is None:
                    continue
                grad = p.grad.data

                state = self.state[p]
                t = state.get("t", 1)
                m: torch.Tensor = state.get("m", torch.zeros_like(p.data, requires_grad=False))
                v: torch.Tensor = state.get("v", torch.zeros_like(p.data, requires_grad=False))
                lr_t = lr * math.sqrt(1 - beta2 ** t) / (1 - beta1 ** t)
                m = beta1 * m + one_minus_beta1 * grad
                v = beta2 * v + one_minus_beta2 * grad * grad

                delta = - weight_decay_scale * p.data - lr_t * m / (torch.sqrt(v) + eps)
                with torch.no_grad():
                    p.add_(delta)

                state["t"] = t + 1
                state["m"] = m
                state["v"] = v

        return loss

def get_lr_cosine(
    t: int,
    lr_max: float,
    lr_min: float,
    warmup_steps: int,
    cosine_steps: int,
) -> float:
    if t < warmup_steps:
        return t * lr_max / warmup_steps
    if t > cosine_steps:
        return lr_min

    return lr_min + 0.5 * (lr_max - lr_min) * (1 + math.cos(math.pi * (t - warmup_steps) / (cosine_steps - warmup_steps)))

def gradient_clipping_(
    parameters: Iterable[torch.nn.Parameter],
    max_l2_norm: float,
    eps=1e-6,
) -> torch.Tensor:
    grads = [p.grad for p in parameters if p.grad is not None]
    assert len(grads), "grads are empty!"
    total_squared_norm = torch.zeros((1,), dtype=grads[0].dtype, device=grads[0].device)
    for g in grads:
        total_squared_norm += torch.linalg.norm(g) ** 2
    norm = total_squared_norm.sqrt()
    if norm >= max_l2_norm:
        norm += eps
        with torch.no_grad():
            for p in parameters:
                if p.grad is not None:
                    p.grad.mul_(max_l2_norm / norm)
    return norm

