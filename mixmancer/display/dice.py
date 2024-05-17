import pygame
import random
from typing import Any
import json
import os


class Dice(pygame.sprite.Sprite):
    def __init__(self, value: int, sheet_list: list[str], roll: int):
        super().__init__()
        self.image = pygame.Surface([100, 100])
        self.image.fill(pygame.color.Color(0, 255, 0))
        self.rect = self.image.get_rect()
        self.roll = roll
        self.sprite_sheets = self.load_spritesheets(sheet_list)
        self.sheet_index, self.sprite_index = 0, 0
        self.last_sheet = len(sheet_list) - 1
        self.end_flag = False
        # Direction? Velocity? Rotation? Speed slows?

    def load_spritesheets(self, sheet_list: list[str]):
        sprite_sheets: list[Spritesheet] = []
        for sheet in sheet_list:
            sprite_sheets.append(Spritesheet(sheet))
        return sprite_sheets

    def update(self, *args: Any, dt: int, **kwargs: Any):
        if not self.end_flag:
            self.image, next_sheet = self.sprite_sheets[self.sheet_index].get_sprite(str(self.sprite_index))
            if next_sheet:
                if self.sheet_index != self.last_sheet:
                    self.sheet_index += 1
                    self.sprite_index = 0
                else:
                    self.end_flag = True
            else:
                self.sprite_index += 1

        if self.sheet_index != self.last_sheet:
            # Movement
            self.rect.x += 10
            self.rect.y += 10


def generate_dice(dice: str) -> Dice:
    """
    Generates a dice object with the specified number of sides.

    Parameters:
        dice (str): A string representing the type of dice (e.g., "d20").

    Returns:
        Dice: A Dice object representing the generated dice.

    Raises:
        ValueError: If the provided 'dice' string is not in the correct format.
        KeyError: If the specified dice value is not found in the 'sprite_sheets' dictionary.
    """
    try:
        val = int(dice.replace("d", ""))
    except ValueError:
        raise ValueError(
            "Invalid dice format. Expected format: 'dx', where x is an integer representing the number of sides."
        )

    roll = random.randint(1, val)
    sprite_path = "assets/dice"
    sprite_sheets = {
        20: ["d20/single_roll.png", f"d20/d20_{roll}.png"],
    }

    if val not in sprite_sheets:
        raise KeyError(f"Dice with {val} sides not found in the sprite_sheets dictionary.")

    sheet_paths = [os.path.join(sprite_path, sheet) for sheet in sprite_sheets[val]]
    return Dice(val, sheet_paths, roll)


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
