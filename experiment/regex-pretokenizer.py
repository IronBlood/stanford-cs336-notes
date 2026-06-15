import regex as re

pat = r"""'(?:[sdmt]|ll|ve|re)| ?\p{L}++| ?\p{N}++| ?[^\s\p{L}\p{N}]++|\s++$|\s+(?!\S)|\s"""

print(re.findall(pat, "that's very nice"))
print(re.findall(pat, "Do you love dogs? I love dogs!"))
