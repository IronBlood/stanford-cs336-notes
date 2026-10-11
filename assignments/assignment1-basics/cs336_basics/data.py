import os
import typing
import numpy as np
import numpy.typing as npt
import torch

def get_batch(
    dataset: npt.NDArray,
    batch_size: int,
    context_length: int,
    device: str,
) -> tuple[torch.Tensor, torch.Tensor]:
    dataset_len = dataset.shape[0]
    xs = []
    ys = []

    for _ in range(batch_size):
        i = np.random.randint(0, dataset_len - context_length)

        x = dataset[i : i + context_length]
        y = dataset[i + 1 : i + context_length + 1]

        xs.append(x)
        ys.append(y)

    x_tensor = torch.tensor(
        np.stack(xs),
        dtype=torch.long,
        device=device,
    )
    y_tensor = torch.tensor(
        np.stack(ys),
        dtype=torch.long,
        device=device,
    )
    return x_tensor, y_tensor

def save_checkpoint(
    model: torch.nn.Module,
    optimizer: torch.optim.Optimizer,
    iteration: int,
    out: str | os.PathLike | typing.BinaryIO | typing.IO[bytes],
) -> None:
    """Save model and optimizer state together with the completed iteration count."""
    checkpoint = {
        "model": model.state_dict(),
        "optimizer": optimizer.state_dict(),
        "iteration": iteration,
    }
    torch.save(checkpoint, out)

def load_checkpoint(
    src: str | os.PathLike | typing.BinaryIO | typing.IO[bytes],
    model: torch.nn.Module,
    optimizer: typing.Optional[torch.optim.Optimizer]=None,
) -> int:
    """Restore model and optimizer state and return the saved iteration count."""
    checkpoint = torch.load(src, map_location="cpu", weights_only=True)
    model.load_state_dict(checkpoint["model"])
    if optimizer is not None:
        optimizer.load_state_dict(checkpoint["optimizer"])
    return checkpoint["iteration"]
