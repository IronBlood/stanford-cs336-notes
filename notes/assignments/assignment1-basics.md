# Assignment 1: Basics

## Problem unicode1a

> What Unicode character does `chr(0)` return?

It returns `U+0000`, the null character.

## Problem unicode1b

> How does this character's string representation `(__repr__())` differ from its printed representation?

`print` writes the actual character to stdout. Since `U+0000` is not printable, the terminal usually shows no visible glyph for it. `repr()` returns a debugging representation of the string, so it escapes the null character as `\x00`.

## Problem unicode1c

> What happens when this character occurs in text? It may be helpful to play around with the following in your Python intepreter and see if it  matches your expectations:
>
> ```
> >>> chr(0)
> >>> print(chr(0))
> >>> "a" + chr(0) + "b"
> >>> print("a" + chr(0) + "b")
> ```

The character is inserted in the string as-is. Python does not treat it as a terminator as in C. It remains part of the string even though it is usually invisible when printed.

## Problem unicode2a

> What are some reasons to prefer training out tokenizer on UTF-8 encoded bytes, rather than UTF-16 or UTF-32? It may be helpful to compare the output of these encodings for various input strings.

Short answer:

UTF-8 is prefered because it is the dominant text encoding on the web and it's compact while still being able to represent all Unicode characters. UTF-16 and UTF-32 often introduce extra zero bytes or longer byte sequences for the same text, which makes byte-level tokenization less efficient and wastes tokenizer capacity on encoding artifacts.

## Problem unicode2b

> Consider the following (incorrect) function, which is intended to decode a UTF-8 byte string into a Unicode string. Why is this function incorrect? Provide an example of an input byte string that yields incorrect results.
>
> ```python
> def decode_utf8_bytes_to_str_wrong(bytestring: bytes):
>     return "".join([bytes([b]).decode("utf-8") for b in bytestring])
> decode_utf8_bytes_to_str_wrong("hello".encode("utf-8"))
> ```

The function tries to decode byte by byte. It works for the example input, which are bytes for `"hello"`. Each character also falls into the ASCII code, which is compatible with UTF-8. However there are characters, for example Chinese, Japanese, or `é` which require multiple bytes, decoding byte by byte will fail.

## Problem unicode2c

> Give a two-byte sequence that does not decode to any Unicode character(s).

`b"\xFF\xFF"` does not decode to any Unicode character(s).
