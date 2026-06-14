import torch

x = torch.tensor(3.0, requires_grad=True)
y = x * x + 2 * x + 1

y.backward()

print(y)      # tensor(16., grad_fn=<AddBackward0>)
print(x.grad) # tensor(8.)
