# PyTorch

This page introduces core concepts and APIs from PyTorch briefly.

## torch.Tensor

- Docs: https://docs.pytorch.org/docs/2.13/tensors.html

`Tensor` is the core data type. Inputs, outputs, learning weights, they are all tensors. `Tensor` is a multi-dimensional matrix containing elements of a single data type, similar to `ndarray` in NumPy (see [numpy.md](./numpy.md)).

There are a few ways to create a `Tensor`. To create a tensor with pre-existing data, use [`torch.tensor(data, *, dtype=None, device=None, requires_grad=False, pin_memory=False)`](https://docs.pytorch.org/docs/2.13/generated/torch.tensor.html). There are also a family of [Creation Ops](https://docs.pytorch.org/docs/2.13/torch.html#tensor-creation-ops):

- `torch.zeros`, `torch.ones`, `torch.empty`: they can create a tensor with specific size.
- `torch.*_like`: they create a tensor with the same size and similar types as another tensor.
- `tensor.new_*`: they create a tensor with similar type but different size as another tensor. **NOTE**: these are instance methods.

`torch.tensor()` always copies `data`, but there are ways to used shared data, for example, `torch.from_numpy()` creates a tensor that shares storage with a NumPy array, and `tensor.new_tensor()` returns a new tensor with `data` as the tensor data.

It is discouraged to use the legacy constructor `torch.Tensor` to create a tensor.

## torch.nn.Module

- Docs: https://docs.pytorch.org/docs/2.13/generated/torch.nn.Module.html

The base class for all neural network modules. Models should be subclasses of this class. Modules can contain other modules, which forms a tree structure.

### Module.forward()

The doc says:

> Define the computation performed at every call. Should be overridden by all subclasses.

and also:

> ... one should call the Module instance afterwards instead of this.

**NOTE**: *this* means the `.forward()` function. So how is `forward()` invoked?

```py
class My_Module(torch.nn.Module):
    # omitted
my_module = My_Module()
output = my_module(input)
```

This works because `torch.nn.Module` (source [torch/nn/modules/module.py](https://github.com/pytorch/pytorch/blob/main/torch/nn/modules/module.py)) implements Python's `__call__` mechanism (see [operators](https://docs.python.org/3/library/operator.html)).

A simplified version of the flow is:

```
module(input)
-> Module.__call__
-> Module._wrapped_call_impl
-> Module._call_impl
-> module.forward(input)
```

### Module.load_state_dict()

From [Saving and Loading Models](https://docs.pytorch.org/tutorials/beginner/saving_loading_models.html)

> In PyTorch, the learnable parameters (i.e. weights and biases) of an `torch.nn.Module` model are contained in the model’s *parameters* (accessed with `model.parameters()`). A *state_dict* is simply a Python dictionary object that maps each layer to its parameter tensor.

The `state_dict` can be saved via:

```py
torch.save(model.state_dict(), PATH)
```

And then loaded by:

```py
model = TheModelClass(*args, **kwargs)
model.load_state_dict(torch.load(PATH, weights_only=True))
```

## torch.nn.Parameter

* Docs: https://docs.pytorch.org/docs/2.13/generated/torch.nn.parameter.Parameter.html

> A kind of Tensor that is to be considered a module parameter.
>
> Parameters are Tensor subclasses, ...

Once a `Parameter` is assigned as a `Module` attribute, it is added to the list of parameters of the `Module`, and will show in the iterators like `.parameters()` and `.named_parameters()`. See the example [pytorch-parameter-buffer.py](../../experiment/pytorch-parameter-buffer.py).

A `Parameter` is normally trainable model state. Optimizers usually receive `model.parameters()`, so registered parameters are the tensors updated during training.


## torch.nn.parameter.Buffer

* Docs: https://docs.pytorch.org/docs/2.13/generated/torch.nn.parameter.Buffer.html

> A kind of Tensor that should not be considered a model parameter. For example, BatchNorm’s `running_mean` is not a parameter, but is part of the module’s state.

## torch.nn.init.trunc_normal_

* Docs: https://docs.pytorch.org/docs/2.13/nn.init.html#torch.nn.init.trunc_normal_
* Source: [torch/nn/init.py](https://github.com/pytorch/pytorch/blob/main/torch/nn/init.py)

> Fill the input Tensor with values drawn from a truncated normal distribution.

## Open Questions

1. What are the differences between a `Parameter` and a `Buffer`?
