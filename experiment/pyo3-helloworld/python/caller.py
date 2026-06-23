import pyo3_helloworld

print(pyo3_helloworld.__file__)
print(pyo3_helloworld.helloworld())

pyo3_helloworld.process_strings(["hello", "world", "how", "are", "you", "?"])

a, b = pyo3_helloworld.dummy_return()
# Vec<Vec<u8>> -> list[bytes] [b'\x00\x01\x02\x03']
print(a)
# Vec<(Vec<u8>, Vec<u8>)> -> list[Tuple[bytes, bytes]] [(b'\x00', b'\x01')]
print(b)
