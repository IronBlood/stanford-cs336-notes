---
type: concept
status: draft
course: cs336
tags: [machine-learning, tensors]
---

# Tensor

A tensor is a multi-dimensional array of numbers.

In machine learning, tensors are the basic data container. Inputs, model parameters, intermediate activations, losses, and gradients are usually represented as tensors.

## Basic Examples

People sometimes describe tensors by their rank, meaning the number of axes or dimensions:

- Scalar, rank 0: a single number, such as `42`.
- Vector, rank 1: a one-dimensional array of numbers, such as `[10, 10, 0]`.
- Matrix, rank 2: a two-dimensional table of numbers, such as a grayscale image with shape `[height, width]`.
- Rank-3 tensor: for example, a color image with shape `[height, width, channels]`, where `channels` might be RGB.
- Rank-4 tensor: for example, a batch of color images with shape `[batch, height, width, channels]`.

The word "rank" can mean different things in linear algebra, but in ML framework documentation it often means "number of dimensions". The shape tells us the size along each dimension.

## Why It Matters

ML code is often about keeping tensor shapes correct.

For example, a batch of tokenized text might have shape:

```text
[batch_size, sequence_length]
```

After the model converts token IDs into embeddings, the tensor might have shape:

```text
[batch_size, sequence_length, embedding_dim]
```

Understanding tensors mostly means understanding:

- what each axis represents;
- what the shape is;
- what operation is being applied;
- whether the tensor lives on CPU or GPU;
- whether the tensor is being tracked for gradients.

## Future Related Concepts

- PyTorch
- TensorFlow
- Automatic differentiation
