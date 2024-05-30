import pygame
import random
from typing import Any
import os
import math
from mixmancer.display.sprite import Spritesheet
from mixmancer.config.data_models import Coordinate


class Dice(pygame.sprite.Sprite):
    """
    A sprite representing a dice with animated movement and rotation.

    Attributes:
        roll (int): The initial roll value of the dice.
        bounds (tuple[int, int]): The boundaries within which the dice can move (width, height).
        sprite_sheets (list[Spritesheet]): A list of spritesheets used for the dice's animation.
        sheet_index (int): The current index of the spritesheet being used.
        sprite_index (int): The current index of the sprite in the spritesheet being displayed.
        last_sheet (int): The index of the last spritesheet in sprite_sheets.
        end_flag (bool): Flag indicating whether the animation has ended.
        wisp_flag (bool): Flag indicating whether a result wisp has spawned off the dice.
        initial_velocity (pygame.Vector2): The initial velocity vector of the dice.
        velocity (pygame.Vector2): The current velocity vector of the dice.
        damping (float): Damping factor applied to the dice's velocity.
        w (int): Width of the dice.
        h (int): Height of the dice.
        x (int): Current x position of the dice.
        y (int): Current y position of the dice.
        rect (pygame.Rect): The rectangle representing the dice's position and size.
        rotation (int): The rotation angle of the dice.

    Methods:
        initialize_position() -> tuple[int, int]:
            Initializes and returns a random valid position within the bounds.

        check_valid_spawn(current_positions: list[tuple[int, int]]) -> bool:
            Checks if the dice can be spawned at its current position without overlapping others.

        load_spritesheets(sheet_list: list[str]) -> list[Spritesheet]:
            Loads and returns the spritesheets from the given list of file paths.

        update(*args: Any, dt: int, **kwargs: Any):
            Updates the sprite's animation and movement based on the elapsed time (dt).
    """

    def __init__(
        self,
        sheet_list: list[str],
        roll: int,
        bounds: Coordinate,
        other_dice: list[Coordinate],
    ):
        """
        Initializes the Dice sprite.

        Args:
            sheet_list (list[str]): List of file paths to the sprite sheets.
            roll (int): The roll value of the dice.
            bounds (tuple[int, int]): The boundaries for the dice's movement (width, height).
            other_dice (list[tuple[int, int]]): List of current positions of other dice to avoid overlap.
        """
        super().__init__()
        self.roll = roll
        self.bounds = bounds
        self.sprite_sheets = self.load_spritesheets(sheet_list)
        self.sheet_index, self.sprite_index = 0, 0
        self.last_sheet = len(sheet_list) - 1
        self.end_flag = False
        self.wisp_flag = False
        self.rotation = random.randint(0, 360)
        self.initial_velocity = pygame.Vector2(random.randint(20, 60), random.randint(20, 60))
        self.velocity = self.initial_velocity.copy()
        self.damping = 1
        self.w, self.h = 100, 100

        # Initialize starting position, velocity, and direction
        while True:  # Keep trying until valid
            self.x, self.y = self.initialize_position()
            self.rect = pygame.Rect(self.x, self.y, self.w, self.h)
            if self.check_valid_spawn(self.rect, other_dice):
                break

    def initialize_position(self) -> tuple[int, int]:
        """
        Initializes a random position for the dice within the bounds.

        Returns:
            tuple[int, int]: A tuple containing the x and y coordinates of the initialized position.
        """
        if random.choices([True, False], weights=self.bounds()):
            if random.choice([True, False]):
                x, y = random.randint(0, self.bounds.x - self.w), 0
            else:
                x, y = random.randint(0, self.bounds.x - self.w), self.bounds.y - self.h
        else:
            if random.choice([True, False]):
                x, y = 0, random.randint(0, self.bounds.y - self.h)
            else:
                x, y = self.bounds.x - self.w, random.randint(0, self.bounds.y - self.h)
        return x, y

    def check_valid_spawn(self, rect: pygame.Rect, other_dice: list[Coordinate]) -> bool:
        """
        Checks if the current position is valid and does not overlap with other dice.

        Args:
            other_dice (list[tuple[int, int]]): A list of tuples containing the positions of other dice.

        Returns:
            bool: True if the position is valid, False otherwise.
        """
        if other_dice:
            for other in other_dice:
                another_dice = pygame.Rect(other.x, other.y, rect.w, rect.h)
                if rect.colliderect(another_dice):
                    return False
        return True

    def load_spritesheets(self, sheet_list: list[str]):
        """
        Loads the sprite sheets from the given list of file paths.

        Args:
            sheet_list (list[str]): List of file paths to the sprite sheets.

        Returns:
            list[Spritesheet]: A list of Spritesheet objects loaded from the file paths.
        """
        sprite_sheets: list[Spritesheet] = []
        for sheet in sheet_list:
            sprite_sheets.append(Spritesheet(sheet))
        return sprite_sheets

    def update_position(self):
        """
        Updates the position of the dice based on its current velocity and checks for boundary collisions.

        The position is adjusted by the current velocity, and the velocity is inverted if the dice hits the bounds.
        The velocity decays over time based on the progress of the animation.
        """
        if self.sheet_index != self.last_sheet:

            self.x += self.velocity.x
            self.y += self.velocity.y

            if self.x + self.w + self.velocity.x > self.bounds.x or self.x + self.velocity.x < 0:
                self.velocity.x = -self.velocity.x
            elif self.y + self.h + self.velocity.y > self.bounds.y or self.y + self.velocity.y < 0:
                self.velocity.y = -self.velocity.y

            decay_factor = 1 - (self.sprite_index / self.sprite_sheets[self.sheet_index].get_frame_count())

            self.velocity = pygame.Vector2(
                math.copysign(1, self.velocity.x) * self.initial_velocity.x * decay_factor,
                math.copysign(1, self.velocity.y) * self.initial_velocity.y * decay_factor,
            )

            self.rect = pygame.Rect(self.x, self.y, self.w, self.h)

    def update(self, *args: Any, **kwargs: Any):
        """Updates the sprite's animation and movement."""
        if not self.end_flag:
            self.image, next_sheet = self.sprite_sheets[self.sheet_index].get_sprite(str(self.sprite_index))
            self.image = pygame.transform.scale(self.image, (self.w, self.h))
            if next_sheet:
                if self.sheet_index != self.last_sheet:
                    self.image = pygame.transform.rotate(self.image, angle=self.rotation)
                    self.sheet_index += 1
                    self.sprite_index = 0
                else:
                    self.end_flag = True
            else:
                self.sprite_index += 1
        self.update_position()


def generate_dice(dice: str, bounds: Coordinate, current_positions: list[Coordinate]) -> Dice:
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
    return Dice(sheet_paths, roll, bounds, current_positions)
