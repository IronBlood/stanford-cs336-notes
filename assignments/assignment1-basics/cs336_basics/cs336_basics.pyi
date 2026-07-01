from collections.abc import Sequence
from os import PathLike
from typing import final

@final
class Tokenizer:
    def __new__(cls, /, vocab: "dict[int, bytes]", merges: "list[tuple[bytes, bytes]]", special_tokens: "list[str] | None") -> "Tokenizer": ...
    def decode(self, /, ids: Sequence[int]) -> str: ...
    def encode(self, /, text: str) -> list[int]: ...

def bpe(input_path: str |PathLike[str], vocab_size: int, special_tokens: Sequence[str], vocab_path: str |PathLike[str], merges_path: str |PathLike[str]) -> None:
    """
    This API is the actual one which will be mainly used with custom defined formats
    of vocabs and merges. The format might be changed in the future.
    """

def bpe_with_special_token_merged(input_path: str |PathLike[str], vocab_size: int, special_tokens: Sequence[str]) -> tuple[dict[int, bytes], list[tuple[bytes, bytes]]]:
    """
    This API is purely for the assignment `train_bpe`, the test cases require special_tokens
    to be inserted in the vocabulary.
    """
