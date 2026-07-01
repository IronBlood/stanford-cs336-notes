import tiktoken
import pathlib

FIXTURES_PATH = pathlib.Path(__file__).resolve().parent / "tests/fixtures"
VOCAB_PATH = FIXTURES_PATH / "gpt2_vocab.json"
MERGES_PATH = FIXTURES_PATH / "gpt2_merges.txt"
ADDRESS_PATH = FIXTURES_PATH / "tinystories_sample.txt"

def test_matches_tiktoken():
    reference_tokenizer = tiktoken.get_encoding("gpt2")
    with open(ADDRESS_PATH) as f:
        test_string = f.read()
    # test_string = "Hello, how <|endoftext|><|endoftext|> are you?<|endoftext|>"
    #reference_ids = reference_tokenizer.encode(test_string, allowed_special={"<|endoftext|>", "<|endoftext|><|endoftext|>"})
    # test_string = "!”"
    reference_ids = reference_tokenizer.encode(test_string, allowed_special={"<|endoftext|>"})
    print("== result ==")
    print(reference_ids)
    print("")
    # reference_tokenizer.decode(reference_ids)


def main():
    test_matches_tiktoken()

if __name__ == "__main__":
    main()
