r"""Train a Transformer LM on memory-mapped raw little-endian uint16 token files.

Short test run (inside the container, from assignments/assignment1-basics):

    uv run python -m cs336_basics.train \
        --train-data /path/to/train.bin \
        --valid-data /path/to/valid.bin \
        --output-dir artifacts/smoke-test \
        --device cuda:0 \
        --batch-size 8 \
        --steps 20 \
        --warmup-steps 2 \
        --eval-every 10 \
        --eval-batches 2 \
        --save-every 10

Replace the data paths with paths accessible inside the container.
For a full run, omit --steps and tune --warmup-steps and optimizer settings.
Use --device cpu for CPU training.
To resume, add --resume PATH and keep the same model architecture settings;
--steps is the total target step count, including completed steps.

Metrics are appended to output-dir/metrics.jsonl. elapsed_seconds measures time
since this session's training loop began, including evaluation and saving.
duration_seconds measures the training interval or individual event duration.
Each invocation has a separate session_id and records its configuration.
tokens_processed assumes the batch size and context length are unchanged on resume.
"""

import argparse
import json
import math
import time
from pathlib import Path
from uuid import uuid4

import numpy as np
import torch

from .data import get_batch, load_checkpoint, save_checkpoint
from .nn import TransformerLM
from .training import AdamW, cross_entropy, get_lr_cosine, gradient_clipping_


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--train-data", type=Path, required=True)
    parser.add_argument("--valid-data", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--resume", type=Path)
    parser.add_argument("--device", default="cpu")
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--vocab-size", type=int, default=10000)
    parser.add_argument("--context-length", type=int, default=256)
    parser.add_argument("--d-model", type=int, default=512)
    parser.add_argument("--d-ff", type=int, default=1344)
    parser.add_argument("--num-layers", type=int, default=4)
    parser.add_argument("--num-heads", type=int, default=16)
    parser.add_argument("--rope-theta", type=float, default=10000.0)
    parser.add_argument("--batch-size", type=int, default=8)
    parser.add_argument("--total-tokens", type=int, default=327680000)
    parser.add_argument("--steps", type=int, help="Override the total-token budget.")
    parser.add_argument("--lr", type=float, default=1e-3)
    parser.add_argument("--min-lr", type=float, default=1e-4)
    parser.add_argument("--warmup-steps", type=int, default=100)
    parser.add_argument("--beta1", type=float, default=0.9)
    parser.add_argument("--beta2", type=float, default=0.999)
    parser.add_argument("--eps", type=float, default=1e-8)
    parser.add_argument("--weight-decay", type=float, default=0.01)
    parser.add_argument("--max-grad-norm", type=float, default=1.0)
    parser.add_argument("--log-every", type=int, default=10)
    parser.add_argument("--eval-every", type=int, default=500)
    parser.add_argument("--eval-batches", type=int, default=10)
    parser.add_argument("--save-every", type=int, default=1000)
    args = parser.parse_args()
    positive = (
        "vocab_size",
        "context_length",
        "d_model",
        "d_ff",
        "num_layers",
        "num_heads",
        "batch_size",
        "total_tokens",
        "log_every",
        "eval_every",
        "eval_batches",
        "save_every",
    )
    for name in positive:
        if getattr(args, name) <= 0:
            parser.error(f"--{name.replace('_', '-')} must be positive")
    if args.steps is None:
        args.steps = math.ceil(args.total_tokens / (args.batch_size * args.context_length))
    if args.steps <= 0 or not 0 <= args.warmup_steps < args.steps:
        parser.error("steps must be positive and 0 <= warmup-steps < steps")
    if args.d_model % args.num_heads or (args.d_model // args.num_heads) % 2:
        parser.error("d-model must be divisible by num-heads, with an even head dimension")
    if not 0 <= args.min_lr <= args.lr:
        parser.error("require 0 <= min-lr <= lr")
    if not (0 <= args.beta1 < 1 and 0 <= args.beta2 < 1):
        parser.error("AdamW betas must be in [0, 1)")
    if args.eps <= 0 or args.max_grad_norm <= 0 or args.weight_decay < 0 or args.rope_theta <= 0:
        parser.error("eps, max-grad-norm, and rope-theta must be positive; weight-decay must be nonnegative")
    return args


def load_tokens(path: Path, context_length: int) -> np.ndarray:
    file_size = path.stat().st_size
    if file_size % 2:
        raise ValueError(f"{path}: uint16 token file must contain an even number of bytes")
    if file_size // 2 <= context_length:
        raise ValueError(f"{path}: need more than context_length tokens")
    return np.memmap(path, dtype="<u2", mode="r")


def batch_loss(model: TransformerLM, dataset: np.ndarray, args: argparse.Namespace) -> torch.Tensor:
    inputs, targets = get_batch(
        dataset,
        args.batch_size,
        args.context_length,
        args.device
    )
    if inputs.min().item() < 0 or inputs.max().item() >= args.vocab_size:
        raise ValueError("Sampled input token IDs are outside the configured vocabulary")
    if targets.min().item() < 0 or targets.max().item() >= args.vocab_size:
        raise ValueError("Sampled target token IDs are outside the configured vocabulary")
    logits = model(inputs)
    return cross_entropy(logits.reshape(-1, args.vocab_size), targets.reshape(-1))


@torch.no_grad()
def evaluate(model: TransformerLM, dataset: np.ndarray, args: argparse.Namespace) -> float:
    was_training = model.training
    # Validation uses a separate sampling stream so its frequency does not change training batches.
    random_state = np.random.get_state()
    model.eval()
    try:
        np.random.seed(args.seed + 1)
        losses = [batch_loss(model, dataset, args).item() for _ in range(args.eval_batches)]
        return sum(losses) / len(losses)
    finally:
        np.random.set_state(random_state)
        model.train(was_training)


def synchronize(device: torch.device) -> None:
    if device.type == "cuda":
        torch.cuda.synchronize(device)
    elif device.type == "mps":
        torch.mps.synchronize()


def main() -> None:
    args = parse_args()
    np.random.seed(args.seed)
    torch.manual_seed(args.seed)
    device = torch.device(args.device)
    train_data = load_tokens(args.train_data, args.context_length)
    valid_data = load_tokens(args.valid_data, args.context_length)
    model = TransformerLM(
        vocab_size=args.vocab_size,
        context_length=args.context_length,
        d_model=args.d_model,
        num_layers=args.num_layers,
        num_heads=args.num_heads,
        d_ff=args.d_ff,
        rope_theta=args.rope_theta,
        device=device,
        dtype=torch.float32,
    )
    parameters = list(model.parameters())
    optimizer = AdamW(
        parameters,
        lr=args.lr,
        betas=(args.beta1, args.beta2),
        eps=args.eps,
        weight_decay=args.weight_decay
    )
    start = 0 if args.resume is None else load_checkpoint(args.resume, model, optimizer)
    if not 0 <= start < args.steps:
        raise ValueError("Checkpoint iteration must be nonnegative and smaller than --steps")
    args.output_dir.mkdir(parents=True, exist_ok=True)
    config = {name: str(value) if isinstance(value, Path) else value for name, value in vars(args).items()}
    with (args.output_dir / f"config-{start}.json").open("w") as handle:
        json.dump(config, handle, indent=2)
    print(f"parameters={sum(p.numel() for p in parameters):,} device={device} steps={args.steps}", flush=True)
    if args.resume is not None:
        print("Resuming weights, optimizer, and iteration; random sampling state is not restored.", flush=True)
    model.train()
    loss_sum = 0.0
    interval_steps = 0
    interval_duration = 0.0
    synchronize(device)
    session_start = time.perf_counter()
    session_id = uuid4().hex
    metrics_path = args.output_dir / "metrics.jsonl"
    tokens_per_step = args.batch_size * args.context_length

    def record_metrics(event: str, completed: int, duration: float, **values) -> None:
        record = {
            "schema_version": 1,
            "session_id": session_id,
            "session_start_step": start,
            "event": event,
            "step": completed,
            "tokens_processed": completed * tokens_per_step,
            "session_tokens_processed": (completed - start) * tokens_per_step,
            "elapsed_seconds": time.perf_counter() - session_start,
            "duration_seconds": duration,
            **values,
        }
        with metrics_path.open("a") as handle:
            handle.write(json.dumps(record, allow_nan=False) + "\n")
            handle.flush()

    record_metrics("session_start", start, 0.0, config=config)
    for step in range(start, args.steps):
        step_start = time.perf_counter()
        lr = get_lr_cosine(step, args.lr, args.min_lr, args.warmup_steps, args.steps)
        for group in optimizer.param_groups:
            group["lr"] = lr
        optimizer.zero_grad(set_to_none=True)
        loss = batch_loss(model, train_data, args)
        if not torch.isfinite(loss).item():
            raise RuntimeError(f"Non-finite training loss at step {step + 1}")
        loss.backward()
        grad_norm = gradient_clipping_(parameters, args.max_grad_norm)
        if not torch.isfinite(grad_norm).all().item():
            raise RuntimeError(f"Non-finite gradient norm at step {step + 1}")
        optimizer.step()
        completed = step + 1
        loss_sum += loss.item()
        interval_steps += 1
        interval_duration += time.perf_counter() - step_start
        if completed % args.log_every == 0 or completed == args.steps:
            synchronize(device)
            throughput = interval_steps * tokens_per_step / interval_duration
            record_metrics(
                "train", completed, interval_duration,
                interval_steps=interval_steps,
                loss=loss_sum / interval_steps,
                lr=lr,
                grad_norm=grad_norm.item(),
                tokens_per_second=throughput,
            )
            print(
                f"step={completed} train_loss={loss_sum / interval_steps:.4f} "
                f"lr={lr:.6g} grad_norm={grad_norm.item():.4f} tokens_per_second={throughput:.0f}",
                flush=True,
            )
            loss_sum = 0.0
            interval_steps = 0
            interval_duration = 0.0
        if completed % args.eval_every == 0 or completed == args.steps:
            synchronize(device)
            validation_start = time.perf_counter()
            valid_loss = evaluate(model, valid_data, args)
            synchronize(device)
            validation_duration = time.perf_counter() - validation_start
            perplexity = math.exp(valid_loss) if valid_loss < 700 else math.inf
            record_metrics(
                "validation", completed, validation_duration,
                loss=valid_loss if math.isfinite(valid_loss) else None,
                perplexity=perplexity if math.isfinite(perplexity) else None,
                eval_batches=args.eval_batches,
                evaluated_tokens=args.eval_batches * tokens_per_step,
            )
            print(f"step={completed} valid_loss={valid_loss:.4f} perplexity={perplexity:.2f}", flush=True)
        if completed % args.save_every == 0 or completed == args.steps:
            checkpoint_path = args.output_dir / f"checkpoint-{completed}.pt"
            checkpoint_start = time.perf_counter()
            save_checkpoint(model, optimizer, completed, checkpoint_path)
            record_metrics(
                "checkpoint", completed, time.perf_counter() - checkpoint_start,
                path=str(checkpoint_path),
            )
            print(f"checkpoint={checkpoint_path}", flush=True)
    record_metrics("session_end", args.steps, time.perf_counter() - session_start)


if __name__ == "__main__":
    main()
