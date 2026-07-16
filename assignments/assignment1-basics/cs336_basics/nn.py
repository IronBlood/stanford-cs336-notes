import torch
from jaxtyping import Float

class Linear(torch.nn.Module):
    def __init__(self, in_features: int, out_features: int, device: torch.device|None = None, dtype: torch.dtype | None=None):
        """
        in_features: final dimension of the input
        out_features: final dimension of the output
        """
        super().__init__()
        self.in_features = in_features
        self.out_features = out_features
        self.weight = torch.nn.Parameter(torch.empty(
            out_features,
            in_features,
            device=device,
            dtype=dtype,
        ))

        sigma = (2.0 / (in_features + out_features)) ** 0.5
        torch.nn.init.trunc_normal_(self.weight, std=sigma, a=-3 * sigma, b=3*sigma)

    def forward(self, x: Float[torch.Tensor, " ... d_in"]) -> Float[torch.Tensor, " ... d_out"]:
        return x @ self.weight.T
