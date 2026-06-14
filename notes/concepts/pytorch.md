---
type: concept
status: stub
course: cs336
tags: [machine-learning, frameworks]
---

# PyTorch

PyTorch is a machine learning framework commonly used for research, teaching, and modern deep learning implementations.

For this course, PyTorch is likely to be the main framework used for assignments and experiments. This page should grow as we encounter concrete PyTorch concepts in code.

## Beginner Mental Model

PyTorch lets Python programs work with [tensors](tensor.md), run operations on CPU or GPU, and automatically compute gradients for training neural networks.

A typical PyTorch training loop looks roughly like this:

```text
make predictions
compute loss
compute gradients
update parameters
repeat
```

In code, this often corresponds to:

```text
output = model(input)
loss = loss_function(output, target)
loss.backward()
optimizer.step()
optimizer.zero_grad()
```

This is not enough to understand PyTorch deeply, but it gives the basic rhythm.

## Why It Matters

PyTorch is useful for learning language models from scratch because it keeps many mechanics visible:

- tensor shapes;
- model layers;
- forward passes;
- loss computation;
- gradients;
- parameter updates;
- training loops.

## Related Concepts To Add Later

- `torch.Tensor`
- `nn.Module`
- `forward`
- `autograd`
- `loss.backward()`
- `optimizer.step()`
- CPU vs GPU devices

## Questions

- What is the difference between a tensor and a model parameter?
- What does `loss.backward()` actually compute?
- What does an optimizer update?
- How are PyTorch modules organized?

