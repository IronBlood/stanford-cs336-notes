import torch
from jaxtyping import Float

class Linear(torch.nn.Module):
    def __init__(self, d_in: int, d_out: int):
        super().__init__()
        self.weight = torch.nn.Parameter(torch.empty(d_out, d_in))

    def forward(self, x: Float[torch.Tensor, " ... d_in"]) -> Float[torch.Tensor, " ... d_out"]:
        return x @ self.weight.T
