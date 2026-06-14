---
type: concept
status: draft
course: cs336
tags: [machine-learning, frameworks]
---

# TensorFlow

TensorFlow is a machine learning framework originally developed by Google. It provides tools for tensor computation, automatic differentiation, neural network layers, training, saving models, and deployment.

In the GPT-2 context, TensorFlow matters mostly as historical background: the original GPT-2 code from OpenAI used TensorFlow, while many modern tutorials and research implementations use [PyTorch](pytorch.md).

## Beginner Mental Model

A machine learning framework usually needs to do a few jobs:

1. Store data and parameters as [tensors](tensor.md).
2. Run tensor operations efficiently, often on GPUs.
3. Track computations so gradients can be computed automatically.
4. Provide building blocks for neural networks.
5. Provide tools for training, saving, and deploying models.

TensorFlow can do all of these.

## TensorFlow 1.x vs TensorFlow 2.x

The important beginner distinction is historical.

TensorFlow 1.x was graph-first:

1. Define a computation graph.
2. Start a session.
3. Feed data into the graph.
4. Ask TensorFlow to execute part of the graph.

This style could be powerful, but it often felt indirect to people used to normal Python programs. Debugging could be awkward because writing the code and running the computation were separate steps.

TensorFlow 2.x moved toward eager execution, where operations run immediately. This style feels closer to ordinary Python and closer to PyTorch.

## What Is A Computation Graph?

A computation graph is a representation of a calculation as nodes and edges.

- Nodes are operations or values.
- Edges show how data flows from one operation to another.

For example, this ordinary Python code:

```python
x = 2
y = 3
z = x + y
print(z)
```

can be thought of as this graph:

```text
x = 2      y = 3
  \        /
   \      /
    add
     |
   z = 5
```

For normal Python, the computation happens immediately when Python reaches `x + y`.

In graph-style TensorFlow, the idea was different: first build a description of the computation, then ask TensorFlow to run it.

A simplified pseudo-example:

```python
x = placeholder()
y = placeholder()
z = add(x, y)

run(z, feed={x: 2, y: 3})  # returns 5
```

The important point is that `z = add(x, y)` does not just mean "compute 2 + 3 right now". It means "create a graph node that will add whatever values are later provided for `x` and `y`."

This graph representation can help a framework analyze, optimize, distribute, save, and deploy the computation. The cost is that the program can feel less direct than ordinary Python.

## Keras

Keras is a high-level neural network API integrated into TensorFlow. For many users, "using TensorFlow" often means writing model code through Keras rather than using lower-level TensorFlow APIs directly.

Keras is useful when you want standard model-building patterns with less boilerplate.

## Why Some Researchers Prefer PyTorch

PyTorch became popular in research and teaching partly because it feels more like regular Python:

- operations execute immediately;
- Python control flow is natural;
- debugging works more like ordinary debugging;
- custom training loops are straightforward.

This does not mean TensorFlow is obsolete or bad. TensorFlow has been widely used in production systems, deployment pipelines, and mobile/web serving. The difference is often about ergonomics and ecosystem preference.

## Connection to This Course

For CS336 and GPT-style models, PyTorch is likely to be the main framework to understand. TensorFlow is still worth knowing because older code, papers, tutorials, and production systems may refer to it.

## Questions

- How do graph-based frameworks optimize a computation graph before running it?
- What is automatic differentiation?
- What did TensorFlow 1.x sessions do?
- How does Keras relate to TensorFlow?
