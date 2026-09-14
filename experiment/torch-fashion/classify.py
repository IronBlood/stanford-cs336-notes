from pathlib import Path

import torch
from torch import nn
from torchvision.transforms import v2
from PIL import Image
import sys
import os

from model import NeuralNetwork
from utils import CURR_DIR

MODEL_PATH = CURR_DIR / "model.1.pth"
IMAGE_DIR = CURR_DIR / "images"

CLASSES = [
    "T-shirt/top", "Trouser", "Pullover", "Dress", "Coat",
    "Sandal", "Shirt", "Sneaker", "Bag", "Ankle boot"
]

def load_image(path: Path | str) -> torch.Tensor:
    image = Image.open(path).convert("L")
    transform = v2.Compose(
        [
            v2.ToImage(),
            v2.Resize((28, 28), antialias=True),
            v2.ToDtype(torch.float32, scale=True),
        ]
    )
    x = transform(image)
    if x.mean() > 0.5:
        x = 1.0 - x
    return x.unsqueeze(0)

device = torch.accelerator.current_accelerator().type if torch.accelerator.is_available() else "cpu"
def classify_image(path: Path | str, model: NeuralNetwork) -> None:
    x = load_image(path).to(device)
    with torch.no_grad():
        logits = model(x)
        probabilities = torch.softmax(logits, dim=1)
        predicted_id = probabilities.argmax(dim=1).item()
        confidence = probabilities[0, predicted_id].item()

    print(f"{CLASSES[predicted_id]} ({confidence:.1%})")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("usage: python classify_image <image_path>")
    else:
        img_path = sys.argv[1]
        model = NeuralNetwork().to(device)
        model.load_state_dict(torch.load(MODEL_PATH, map_location=device))
        model.eval()
        classify_image(img_path, model)
