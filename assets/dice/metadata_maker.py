import json
import os
from PIL import Image
from typing import Any

input_file = input("input file path for png containing sprite frames: ")
pixel_width = int(input("input frame pixel width (int): "))
pixel_height = int(input("input frame pixel height (int): "))
frame_count = int(input("input number of frames in png: "))

output_file = input_file.replace(".png", ".json")
file_name = os.path.basename(input_file).replace("png", "")

image = Image.open(input_file)
image_width, _ = image.size

data: dict[int, dict[str, int]] = {}
x, y = 0, 0
for i in range(frame_count):
    data[i] = {"x": x, "y": y}
    x += pixel_width
    if x == image_width:
        x = 0
        y += pixel_height

output_data: dict[str, Any] = {"frames": data, "dimensions": {"width": pixel_width, "height": pixel_height}}

with open(output_file, "w") as json_file:
    json.dump(output_data, json_file)
