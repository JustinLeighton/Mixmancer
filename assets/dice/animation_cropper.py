import numpy as np
from pathlib import Path
from PIL import Image
import os


def trim_greenscreen_and_crop(image_path: Path, output_path: Path):
    img = Image.open(image_path).convert("RGBA")
    np_img = np.array(img)

    # Define color value thresholds
    green_threshold = 240
    green_red_difference = 100
    green_blue_difference = 50

    # Create a mask based on color value thresholds
    mask = (
        (np_img[:, :, 1] > green_threshold)
        & (np.abs(np_img[:, :, 1] - np_img[:, :, 0]) > green_red_difference)
        & (np.abs(np_img[:, :, 2] - np_img[:, :, 0]) > green_blue_difference)
    )
    np_img[mask] = [0, 0, 0, 0]

    # Use numpy to get the variance across the rows and columns
    row_var = np.var(np_img[:, :, :3], axis=0)
    col_var = np.var(np_img[:, :, :3], axis=1)

    # Crop the image
    no_variance_row = np.where(row_var > 5)
    no_variance_col = np.where(col_var > 5)
    if len(no_variance_row[0]) == 0 or len(no_variance_col[0]) == 0:
        return img.size
    else:
        buffer = 5
        cropped_img = Image.fromarray(np_img).crop(
            (
                no_variance_row[0][0] - buffer,
                no_variance_col[0][0] - buffer,
                no_variance_row[0][-1] + buffer,
                no_variance_col[0][-1] + buffer,
            )
        )
        cropped_img.save(output_path)
    return cropped_img.size


directory = Path("assets/dice/tmp")

cropped_folder = Path(os.path.join(directory, "cropped"))
if not os.path.exists(cropped_folder):
    os.makedirs(cropped_folder)

for filename in os.listdir(directory):
    if filename.lower().endswith(".png"):
        original_file = Path(os.path.join(directory, filename))
        cropped_file = Path(os.path.join(cropped_folder, filename))
        trim_greenscreen_and_crop(original_file, cropped_file)
