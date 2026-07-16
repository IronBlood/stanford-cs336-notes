from pathlib import Path
import torch

CURR_DIR = Path(__file__).resolve().parent
path = CURR_DIR.parent / "output/dummy.pt"

x = torch.tensor([1, 2, 3])
torch.save(x, path)
print(x)

x = torch.load(path, weights_only=True)
print(x)
print(type(x))
