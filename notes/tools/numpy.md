# NumPy

NumPy is short for **Numerical Python**. One of the core features it provides is called **ndarray**, which means N-dimensional array. It is designed for efficiency on large arrays of data.

Python has a built-in data type named `list`. However, it is general-purpose. It can be slow for large numeric arrays, for example the following lines create a list of one million integers, and create another one `my_list2` by doubling each number.

```py
my_list = list(range(1000000))
%time for _ in range(10): my_list2 = [x * 2 for x in my_list]
```

The following lines do the same thing but with NumPy:

```py
import numpy as np
my_arr = np.arange(1000000)
%time for _ in range(10): my_arr2 = my_arr * 2
```

> Note: `%time` is a magic command in IPython and Jupyter Notebooks which tracks the exact execution time.

Running these blocks on Google Colab (which is also built on top of Jupyter Notebook) returned the following results:

```
Python list:
CPU times: user 284 ms, sys: 257 ms, total: 542 ms
Wall time: 546 ms

NumPy ndarray:
CPU times: user 11.5 ms, sys: 9.08 ms, total: 20.6 ms
Wall time: 24.6 ms
```

NumPy is fast because its arrays store values in compact, typed memory buffers. Unlike a Python `list`, a NumPy array usually stores elements of one fixed type, such as `int32`, `float64` or `int64`. Many operations run in optimized native code, implemented mostly in C, instead of Python loops (related concept: [FFI](../concepts/ffi.md)). This is why it became "the cornerstone of numerical computing in Python". (Wes McKinney, *Python for Data Analysis*)
