---
type: dataset
status: draft
course: cs336
tags: [datasets, language-modeling, web-text]
---

# OpenWebText

The original dataset contains 80 files in [parquet](../concepts/parquet.md) format, no text files. Stanford CS336 provided a converted version, can be downloaded with `wget(1)` and then uncompressed, see more from [README.md from assignment 1](../../assignments/assignment1-basics/README.md):

```bash
wget https://huggingface.co/datasets/stanford-cs336/owt-sample/resolve/main/owt_train.txt.gz
gunzip owt_train.txt.gz
wget https://huggingface.co/datasets/stanford-cs336/owt-sample/resolve/main/owt_valid.txt.gz
gunzip owt_valid.txt.gz
```

Then there are:

- `owt_train.txt` 12G
- `owt_valid.txt` 290M

These files were actually generated from the following script:

```py
from datasets import load_dataset
from tqdm import tqdm
import io

dataset = load_dataset("Skylion007/openwebtext")['train']
split_dataset = dataset.train_test_split(train_size=2400000, test_size=60000, seed=0)


with io.open('data/owt_train.txt','w') as fopen:
    listout = []
    for data in tqdm(split_dataset['train']):
        listout.append(data['text']+'<|endoftext|>')
        if len(listout) > 1000:
            _ = fopen.write(''.join(listout))
            listout = []


with io.open('data/owt_valid.txt','w') as fopen:
    listout = []
    for data in tqdm(split_dataset['test']):
        listout.append(data['text']+'<|endoftext|>')
        if len(listout) > 1000:
            _ = fopen.write(''.join(listout))
            listout = []
```

## Sources

- [Hugging Face: Skylion007/openwebtext](https://huggingface.co/datasets/Skylion007/openwebtext)
- [Hugging Face: stanford-cs336/owt-sample](https://huggingface.co/datasets/stanford-cs336/owt-sample)
