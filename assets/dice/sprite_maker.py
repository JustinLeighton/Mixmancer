import os
from PIL import Image
from PIL.Image import Image as ImageType
from pathlib import Path


def create_sprite_sheet(image_folder: Path, output_file: str):
    # Get all image file paths in the folder
    image_files = [os.path.join(image_folder, file) for file in os.listdir(image_folder) if file.endswith("png")]

    if not image_files:
        print("No image files found in the specified folder.")
        return

    # Determine the max width and height of any sprite
    max_width = 0
    max_height = 0
    images: list[ImageType] = []

    for image_file in image_files:
        img = Image.open(image_file)
        images.append(img)
        if img.width > max_width:
            max_width = img.width
        if img.height > max_height:
            max_height = img.height

    # Calculate the dimensions of the sprite sheet
    num_images = len(images)
    num_columns = 4
    num_rows = (num_images + num_columns - 1) // num_columns  # Ceiling division

    sheet_width = num_columns * max_width
    sheet_height = num_rows * max_height

    # Create the sprite sheet image
    sprite_sheet = Image.new("RGBA", (sheet_width, sheet_height))

    # Paste each sprite into the sprite sheet
    for index, img in enumerate(images):
        row = index // num_columns
        col = index % num_columns
        x = col * max_width
        y = row * max_height
        sprite_sheet.paste(img, (x, y))

    # Save the sprite sheet to a file
    sprite_sheet.save(output_file)
    print(f"Sprite sheet saved to {output_file}")


image_folder = Path("path/to/your/sprites")
output_file = "spritesheet.png"
create_sprite_sheet(image_folder, output_file)
