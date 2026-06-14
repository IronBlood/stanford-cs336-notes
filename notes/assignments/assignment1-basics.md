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
