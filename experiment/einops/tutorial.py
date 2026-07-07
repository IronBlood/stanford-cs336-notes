import numpy as np
from pathlib import Path
import numpy.typing as npt
from PIL import Image

CURR_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = CURR_DIR / "output"

def save_bmp(image: npt.NDArray[np.float64], filename: str) -> None:
    """Save one RGB image as a BMP file.

    The input image is expected to have shape `(height, width, 3)` and
    contain float values in the range `[0, 1]`.
    """
    OUTPUT_DIR.mkdir(exist_ok=True)
    output_path = OUTPUT_DIR / filename
    if output_path.exists():
        print(f"skip existing file: {output_path}")
        return

    image_u8 = (image * 255).clip(0, 255).astype(np.uint8)
    Image.fromarray(image_u8, mode="RGB").save(output_path)


images: npt.NDArray[np.float64] = np.load(CURR_DIR / "resources/test_images.npy", allow_pickle=False)

print(images.shape) # (6, 96, 96, 3)
print(images.dtype) # float64

# here `image0` is still `npt.NDArray[np.float64]`, it's just not distinguish
image0: npt.NDArray[np.float64] = images[0]

# inspect to see what data is actually inside
print("min:", image0.min()) # 0.0
print("max:", image0.max()) # 1.0

# dump the top left 2 x 2 pixels
# print(image0[:2, :2])

save_bmp(image0, "image0.bmp")
save_bmp(images[1], "image1.bmp")

from einops import rearrange

image0_transformed = rearrange(image0, "height width color -> width height color")
save_bmp(image0_transformed, "image0_transformed.bmp")

x = rearrange(images, "b h w c -> (b h) w c")
print(x.shape) # (576, 96, 3)
save_bmp(x, "imagex_bh.bmp")

y = rearrange(images, "b h w c -> h (b w) c")
print(y.shape) # (96, 576, 3)
save_bmp(y, "imagex_bw.bmp")

flatten = rearrange(images, "b h w c -> (b h w c)")
print(flatten.shape) # 165888

x = rearrange(images, "(b1 b2) h w c -> b1 b2 h w c", b1=2)
print(x.shape) # (2, 3, 96, 96, 3)

x = rearrange(images, "(b1 b2) h w c -> (b1 h) (b2 w) c", b1=2)
save_bmp(x, "image_two_rows.bmp")

y = rearrange(images, "(b1 b2) h w c -> (b2 h) (b1 w) c", b1=2)
save_bmp(y, "image_two_cols.bmp")
