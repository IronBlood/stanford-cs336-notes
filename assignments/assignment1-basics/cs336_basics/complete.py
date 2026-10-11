import argparse
import sys
import time
import torch
from pathlib import Path

from cs336_basics.data import load_checkpoint
from cs336_basics.nn import TransformerLM

from .cs336_basics import Tokenizer

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--model-path", type=Path, required=True)
    parser.add_argument("--vocab-path", type=Path, required=True)
    parser.add_argument("--merges-path", type=Path, required=True)
    parser.add_argument("--prompt", type=str, required=True)
    parser.add_argument("--device", default="cpu")
    parser.add_argument("--vocab-size", type=int, default=10000)
    parser.add_argument("--context-length", type=int, default=256)
    parser.add_argument("--d-model", type=int, default=512)
    parser.add_argument("--d-ff", type=int, default=1344)
    parser.add_argument("--num-layers", type=int, default=4)
    parser.add_argument("--num-heads", type=int, default=16)
    parser.add_argument("--rope-theta", type=float, default=10000.0)
    parser.add_argument("--max-tokens", type=int, default=1024)
    parser.add_argument("--temperature", type=float, default=1.0)
    parser.add_argument("--top-p", type=float, default=1.0)

    args = parser.parse_args()

    positive = (
        "vocab_size",
        "context_length",
        "d_model",
        "d_ff",
        "num_layers",
        "num_heads",
        "rope_theta",
        "temperature",
        "max_tokens",
    )
    for name in positive:
        if getattr(args, name) <= 0:
            parser.error(f"--{name.replace('_', '-')} must be positive")

    if args.top_p is not None:
        if args.top_p <= 0 or args.top_p > 1:
            parser.error("--top-p must be in range (0, 1]")

    if args.d_model % args.num_heads or (args.d_model // args.num_heads) % 2:
        parser.error("d-model must be divisible by num-heads, with an even head dimension")

    return args

@torch.no_grad()
def gen(
    model: TransformerLM,
    tokenizer: Tokenizer,
    text: str,
    context_length: int,
    max_tokens: int,
    temperature: float,
    top_p: float,
    device: torch.device,
) -> str:
    token_ids = tokenizer.encode(text)
    prompt_length = len(token_ids)
    if device.type == "cuda":
        torch.cuda.synchronize(device)
    started = time.perf_counter()

    for _ in range(max_tokens):
        x = torch.tensor(
            token_ids[-context_length:],
            dtype=torch.long,
            device=device
        )
        x = x.unsqueeze(0)
        logits = model(x)
        probabilities = softmax(logits[0, -1, :], temperature)
        filtered_probs, filtered_token_ids = sorted_probabilities(probabilities, top_p)
        sampled_index = torch.multinomial(filtered_probs, num_samples=1)
        next_token_id = int(filtered_token_ids[sampled_index].item())
        if tokenizer.decode([next_token_id]) == "<|endoftext|>":
            break;
        token_ids.append(next_token_id)

    if device.type == "cuda":
        torch.cuda.synchronize(device)
    elapsed = time.perf_counter() - started
    generated_tokens = len(token_ids) - prompt_length
    print(
        f"generated_tokens={generated_tokens} elapsed_seconds={elapsed:.3f} "
        f"tokens_per_second={generated_tokens / elapsed:.2f}",
        file=sys.stderr,
    )
    return tokenizer.decode(token_ids)

def softmax(logits: torch.Tensor, temperature: float):
    logit_max = logits.max(dim=-1, keepdim=True).values
    shifted = logits - logit_max
    e = torch.exp(shifted / temperature)
    exp_sum = e.sum(dim=-1, keepdim=True)
    return e / exp_sum

def sorted_probabilities(probabilities: torch.Tensor, top_p: float) -> tuple[torch.Tensor, torch.Tensor]:
    sorted_probs, token_ids = torch.sort(probabilities, descending=True)
    cumulative_probs = torch.cumsum(sorted_probs, dim=-1)
    keep = cumulative_probs - sorted_probs < top_p
    filtered_probs = sorted_probs.masked_fill(~keep, 0.0)
    filtered_probs = filtered_probs / filtered_probs.sum()
    return filtered_probs, token_ids

def main() -> None:
    args = parse_args()

    device = torch.device(args.device)
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
    load_checkpoint(args.model_path, model)
    model.eval()

    tokenizer = Tokenizer.load(
        vocab_path=str(args.vocab_path),
        merges_path=str(args.merges_path),
        special_tokens=["<|endoftext|>"]
    )

    print(gen(
        model=model,
        tokenizer=tokenizer,
        text=args.prompt,
        context_length=args.context_length,
        max_tokens=args.max_tokens,
        temperature=args.temperature,
        top_p=args.top_p,
        device=device,
    ))

if __name__ == "__main__":
    main()
