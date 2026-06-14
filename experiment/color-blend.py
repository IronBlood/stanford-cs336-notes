import torch
from pathlib import Path


OUTPUT_DIR = Path("output")

# Implemented by ChatGPT
def save_color_square(color: torch.Tensor, filename: str, size: int = 100) -> Path:
    """Save a square RGB color swatch as a 24-bit BMP image."""
    output_path = OUTPUT_DIR / filename
    if output_path.suffix != ".bmp":
        raise ValueError("Use a .bmp filename for this no-dependency image writer.")

    rgb = color.detach().cpu().flatten()
    if rgb.numel() != 3:
        raise ValueError("Expected an RGB color tensor with exactly 3 values.")

    rgb = rgb.clamp(0, 255).round().to(torch.uint8)
    red, green, blue = rgb.tolist()
    pixel = bytes([blue, green, red])  # BMP stores 24-bit pixels as BGR.

    output_path.parent.mkdir(parents=True, exist_ok=True)

    row_size = size * 3
    row_padding = (4 - row_size % 4) % 4
    row = pixel * size + b"\x00" * row_padding
    pixel_data = row * size

    file_header_size = 14
    dib_header_size = 40
    pixel_offset = file_header_size + dib_header_size
    file_size = pixel_offset + len(pixel_data)

    file_header = (
        b"BM"
        + file_size.to_bytes(4, "little")
        + b"\x00\x00"
        + b"\x00\x00"
        + pixel_offset.to_bytes(4, "little")
    )
    dib_header = (
        dib_header_size.to_bytes(4, "little")
        + size.to_bytes(4, "little", signed=True)
        + size.to_bytes(4, "little", signed=True)
        + (1).to_bytes(2, "little")
        + (24).to_bytes(2, "little")
        + (0).to_bytes(4, "little")
        + len(pixel_data).to_bytes(4, "little")
        + (2835).to_bytes(4, "little", signed=True)
        + (2835).to_bytes(4, "little", signed=True)
        + (0).to_bytes(4, "little")
        + (0).to_bytes(4, "little")
    )

    output_path.write_bytes(file_header + dib_header + pixel_data)
    return output_path


red = torch.tensor([255, 0, 0])
blue = torch.tensor([0, 0, 255])

purple = red * 0.5 + blue * 0.5
print(purple)
print(save_color_square(purple, "purple.bmp"))
