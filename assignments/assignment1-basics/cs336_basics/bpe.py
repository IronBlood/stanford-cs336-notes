import os
from . import cs336_basics

def train_bpe(
    input_path: str | os.PathLike,
    vocab_size: int,
    special_tokens: list[str],
) -> tuple[dict[int, bytes], list[tuple[bytes, bytes]]]:
    if not 256 <= vocab_size <= 0xFFFF:
        raise ValueError("vocab_size must be between [256, 65535]")
    return cs336_basics.bpe(input_path, vocab_size, special_tokens)
