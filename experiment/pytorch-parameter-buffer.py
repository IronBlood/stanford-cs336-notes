import torch


class DummyModule(torch.nn.Module):
    def __init__(self) -> None:
        super().__init__()
        self.weight = torch.nn.Parameter(torch.ones(2, 3))
        self.running_total = torch.nn.parameter.Buffer(torch.zeros(3))

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return x @ self.weight.T


module = DummyModule()

print("parameters:")
for parameter in module.parameters():
    print(parameter)

print("\nnamed parameters:")
for name, parameter in module.named_parameters():
    print(name, parameter)

print("\nbuffers:")
for buffer in module.buffers():
    print(buffer)

print("\nnamed buffers:")
for name, buffer in module.named_buffers():
    print(name, buffer)
