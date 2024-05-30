import pygame
import json
from typing import Any


class Spritesheet:
    """
    A class to handle loading and extracting sprites from a spritesheet image.

    Attributes:
        filename (str): The filename of the spritesheet image.
        metadata (str): The filename of the associated metadata file.
        sprite_sheet (pygame.Surface): The spritesheet image loaded into Pygame surface.
        data (dict): The metadata loaded from the associated JSON file.
        height (int): The height of each sprite frame.
        width (int): The width of each sprite frame.
    """

    def __init__(self, filename: str):
        """
        Initializes the Spritesheet object with the given filename.

        Parameters:
            filename (str): The filename of the spritesheet image.
        """
        self.filename = filename
        self.metadata = self.filename.replace("png", "json")
        self.sprite_sheet = pygame.image.load(filename).convert()
        self.data = self.load_metadata()
        self.height, self.width = self.data["dimensions"]["height"], self.data["dimensions"]["width"]
        self.total_frames = len(self.data["frames"]) - 1

    def load_metadata(self) -> dict[str, Any]:
        """
        Loads the metadata from the associated JSON file.

        Returns:
            dict: The metadata loaded from the JSON file.
        """
        with open(self.metadata) as f:
            data = json.load(f)
        return data

    def get_frame(self, x: int, y: int, w: int, h: int) -> pygame.Surface:
        """
        Extracts a single sprite frame from the spritesheet.

        Parameters:
            x (int): The x-coordinate of the top-left corner of the frame.
            y (int): The y-coordinate of the top-left corner of the frame.
            w (int): The width of the frame.
            h (int): The height of the frame.

        Returns:
            pygame.Surface: The extracted sprite frame as a Pygame surface.
        """
        sprite = pygame.Surface((w, h))
        sprite.set_colorkey((0, 0, 0))
        sprite.blit(self.sprite_sheet, (0, 0), (x, y, w, h))
        return sprite

    def get_frame_count(self) -> int:
        return self.total_frames

    def get_sprite(self, frame: str) -> tuple[pygame.Surface, bool]:
        """
        Retrieves a sprite frame by its name from the spritesheet.

        Parameters:
            frame (str): The name of the frame as specified in the metadata.

        Returns:
            tuple: A tuple containing the sprite frame corresponding to the given name
                and a boolean indicating if it's the last frame.
        """
        x, y = self.data["frames"][frame]["x"], self.data["frames"][frame]["y"]
        image = self.get_frame(x, y, self.width, self.height)
        return image, str(self.total_frames) == frame
