---
type: concept
status: stub
course: cs336
tags: [data-format, datasets]
---

# Parquet

## What It Is

It's a column-oriented data storage format. Commonly the data is stored with the extension `.parquet`.

From a programmer's view, to manipulate this data format, there are several implementations:

- [Java](https://github.com/apache/parquet-java)
- Python: commonly through [pandas](https://pandas.pydata.org/) with a Parquet engine such as [pyarrow](https://pypi.org/project/pyarrow/) or [fastparquet](https://pypi.org/project/fastparquet/).
- [C++](https://github.com/apache/arrow), which also provides bindings to R, Ruby, Python (pyarrow) and Matlab.
- [Rust](https://github.com/apache/arrow-rs)

See this [example](../../experiment/save-load-parquet.py).

## Questions

- Why does Parquet matter for large datasets?

## Related Dataset Pages

- [TinyStories](../datasets/tiny-stories.md)
- [OpenWebText](../datasets/openwebtext.md)

## Sources

- [Apache Parquet](https://parquet.apache.org/)
