import torch

x = torch.ones(3, 4)
y = torch.ones(4, 3)

z = x @ y
print(z)

from einops import einsum

z = einsum(x, y, "seq1 hidden, hidden seq2 -> seq1 seq2")
print(z)
