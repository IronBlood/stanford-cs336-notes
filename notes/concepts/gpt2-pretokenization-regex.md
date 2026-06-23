# GPT-2 Pretokenization Regex

The following regular expression is shown in Assignment 1, which mentions [openai/tiktoken#234](https://github.com/openai/tiktoken/pull/234/changes):

```py
r"""'(?:[sdmt]|ll|ve|re)| ?\p{L}+| ?\p{N}+| ?[^\s\p{L}\p{N}]+|\s+(?!\S)|\s+"""
```

But in the [latest implementation](https://github.com/openai/tiktoken/blob/3591ff175d6a80efbe4fcc7f0e219ddd4b8c52f1/tiktoken_ext/openai_public.py), it is optimized to:

```py
r"""'(?:[sdmt]|ll|ve|re)| ?\p{L}++| ?\p{N}++| ?[^\s\p{L}\p{N}]++|\s++$|\s+(?!\S)|\s"""
```

> NOTE: This page will focus on the latest expression.

The whole expression can be split into smaller chunks. These chunks form one larger alternation separated by `|`.

- `'(?:[sdmt]|ll|ve|re)` contractions
- ` ?\p{L}++` letters
- ` ?\p{N}++` numbers
- ` ?[^\s\p{L}\p{N}]++` punctuation
- `\s++$` trailing whitespace
- `\s+(?!\S)` whitespace before trailing whitespace or end of string
- `\s` one whitespace character

## Contractions

```
'(?:[sdmt]|ll|ve|re)
```

This matches common English contraction endings:

* `'s`: `it's`, `Bob's`
* `'d`: `I'd`
* `'m`: `I'm`
* `'t`: `haven't`, `isn't`
* `'ll`: `I'll`
* `'ve`: `you've`
* `'re`: `you're`

> NOTE: the apostrophe `'` (Unicode `U+0027`) will NOT match other situations, for example the right single quote `’` (Unicode `U+2019`), or modifier letter apostrophe `ʼ` (Unicode `U+02BC`).

`(?:...)` is a non-capturing group. Unlike standard capturing groups `(...)`, a non-capturing group does not create a capture group in the match result. For example with regex `([A-Za-z]+)\s(?:Smith|Jones)` and text `Alice Smith`, it matches but the first capture is `Alice`, `Smith` is required for the match, but it is not captured as a separate group.

## Letters

```
 ?\p{L}++
```

This means:

* an optional ordinary space ` ?`
* followed by one or more Unicode letters `\p{L}++`

Here the term `letters` doesn't mean the ASCII `A-Za-z` only. Any Unicode character in the general category `Letter` matches, for example:

```
hello
café
中文
русский
Ελληνικά
```

The ending `++` is a **possessive quantifier**: one or more, without backtracking. It is similar to +, but after consuming letters, the regex engine will not give any of them back while trying another interpretation.

> NOTE(TODO): needs more explanation about **possessive**.

## Numbers

```
 ?\p{N}++
```

Similar to letters, `\p{N}` matches any character in the Unicode `Number` category, including `123` and `１２３`.

## Punctuation or Symbols

```
 ?[^\s\p{L}\p{N}]++
```

`^` means "anything except", so `[^\s\p{L}\p{N}]` matches punctuation, symbols, and emojis:

- `!`
- `...`
- `+-`
- `🙂`
- `→`

## Trailing Whitespace

```
\s++$
```

`\s` matches any whitespace, `$` means the end of the string. This whole pattern means "one or more whitespace characters at the end of the string" with possessive behavior.

## Whitespace when no non-whitespace follows

```
\s+(?!\S)
```

`(?!\S)` means the next character must not be non-whitespace. Since `\S` means a non-whitespace character, it means that the next position is either:

- followed by whitespace, or
- at the end of the string

For example, given `hello   world` it catches the first two spaces, because:

- `\s+` first tries to consume all three spaces
- but the next character is `w`, which **is** non-whitespace, so the **lookahead** `(?!\S)` fails.
- the engine backtracks: it gives back one space, so now it tries the first two spaces
- now the next character is a space, whi is not `\S`, so this alternative matches the first two spaces.

## One whitespace character

`\s` matches exactly one whitespace character, for example:

- space
- tab `\t`
- newline `\n`
- carriage return `\r`
- other Unicode whitespace characters
