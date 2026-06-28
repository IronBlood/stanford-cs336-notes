import os
from . import cs336_basics
import sys
from pathlib import Path

def train_bpe(
    input_path: str | os.PathLike,
    vocab_size: int,
    special_tokens: list[str],
) -> tuple[dict[int, bytes], list[tuple[bytes, bytes]]]:
    if not 256 <= vocab_size <= 0xFFFF:
        raise ValueError("vocab_size must be between [256, 65535]")
    return cs336_basics.bpe_with_special_token_merged(input_path, vocab_size, special_tokens)

def parse_args() -> tuple[Path, int, Path, Path]:
    if len(sys.argv) != 7:
        raise ValueError(f"usage: {sys.argv[0]} <file_path> <vocab_size> --output-vocab <vocab_path> --output-merges <merges_path>")
    if sys.argv[3] != "--output-vocab" or sys.argv[5] != "--output-merges":
        raise ValueError(f"usage: {sys.argv[0]} <file_path> <vocab_size> --output-vocab <vocab_path> --output-merges <merges_path>")

    file_path = Path(sys.argv[1]).resolve(strict=True)
    vocab_size = int(sys.argv[2])
    vocab_path = Path(sys.argv[4]).resolve(strict=False)
    merges_path = Path(sys.argv[6]).resolve(strict=False)

    return file_path, vocab_size, vocab_path, merges_path

def main() -> None:
    file_path, vocab_size, vocab_path, merges_path = parse_args()
    if not 256 <= vocab_size <= 0xFFFF:
        raise ValueError("vocab_size must be between [256, 65535]")
    cs336_basics.bpe(file_path, vocab_size, ["<|endoftext|>"], vocab_path, merges_path)

if __name__ == "__main__":
    main()
