import pygame
from PIL import Image
import os
from typing import Any
from mixmancer.display.dice import generate_dice, Dice
from mixmancer.display.effects import TextSprite  # , ResultWisp
from mixmancer.config.data_models import DataModel, Coordinate
from mixmancer.config.parameters import FRAME_RATE


class ImageProjector:
    """A class to manage images projected to second display

    Attributes:
        resolution (tuple): A tuple representing the resolution of the display.
        display (int): An integer representing the display number.
        screen (pygame.Surface): A Pygame Surface object representing the screen.
        status (bool): A boolean indicating the status of the projector.
        image (pygame.Surface): A Pygame Surface object representing the loaded image.
    """

    def __init__(self, resolution: Coordinate, display: int):
        """
        Initializes the ImageProjector object with the given resolution and display.

        Args:
            resolution (tuple): A tuple representing the resolution of the display.
            display (int): An integer representing the display number.
        """
        self.resolution = resolution
        self.display = display
        self.screen = pygame.display.set_mode(self.resolution(), flags=pygame.NOFRAME, display=self.display)
        self.status: bool = False
        self.image: pygame.Surface = pygame.Surface(self.resolution())
        self.current_image: str = ""
        self.dice_group: pygame.sprite.Group[Any] = pygame.sprite.Group()
        self.wisp_group: pygame.sprite.Group[Any] = pygame.sprite.Group()
        self.text_group: pygame.sprite.Group[Any] = pygame.sprite.Group()
        self.sprite_groups = [self.dice_group, self.wisp_group, self.text_group]
        self.dice_timer: int = 0
        self.dice_result: int = 0
        self.dice_expiration: int = 10 * FRAME_RATE

    def spawn_wisp(self, dice: Dice):
        if dice.end_flag and not dice.wisp_flag:
            dice.wisp_flag = True
            # self.wisp_group.add(ResultWisp((dice.rect.x, dice.rect.y), self.resolution.half()))
            self.text_group.add(TextSprite(str(self.dice_result), self.resolution.half()))

    def spawn_dice(self, **kwargs: int):
        """
        Spawn dice objects for a die-roll from hedgebot.

        Parameters:
            **kwargs (int): Keyword arguments representing the count of each type of dice to add.
                Supported dice types: 'd4', 'd6', 'd8', 'd10', 'd12', 'd20', 'd100'.
        """
        self.clear_dice()
        self.dice_timer = 1
        results: list[int] = []
        for dice in ["d4", "d6", "d8", "d10", "d12", "d20", "d100"]:
            if dice in kwargs.keys():
                for _ in range(kwargs[dice]):
                    current_pos = [Coordinate(d.rect.x, d.rect.y) for d in self.dice_group]
                    new_dice = generate_dice(dice, self.resolution, current_pos)
                    self.dice_group.add(new_dice)
                    results.append(new_dice.roll)
        modifier = kwargs.get("modifier", 0)
        if kwargs.get("advantage", False):
            self.dice_result = max(results) + modifier
        elif kwargs.get("disadvantage", False):
            self.dice_result = min(results) + modifier
        else:
            self.dice_result = sum(results) + modifier
        print("Roll result:", self.dice_result)

    def update_dice(self):
        """
        Updates the state of all dice objects in the dice group.

        Parameters:
            dt (int): The time elapsed since the last update, in milliseconds.
        """
        if self.dice_timer:
            self.dice_timer += 1
            # print("Roll timer:", self.dice_expiration - self.dice_timer)
            if self.dice_timer > self.dice_expiration:
                self.clear_dice()
            else:
                self.check_collisions()
                for group in self.sprite_groups:
                    group.update()

    def draw_dice(self):
        for group in self.sprite_groups:
            group.draw(self.screen)

    def check_collisions(self):
        collisions = pygame.sprite.groupcollide(self.dice_group, self.dice_group, False, False)
        collision_tracking: list[Any] = []
        for dice1, dice2_list in collisions.items():
            collision_tracking.append(dice1)
            self.spawn_wisp(dice1)
            for dice2 in dice2_list:
                if dice2 not in collision_tracking:
                    if abs(dice1.rect.centerx - dice2.rect.centerx) > abs(dice1.rect.centery - dice2.rect.centery):
                        dice1.velocity.x, dice2.velocity.x = -dice1.velocity.x, -dice2.velocity.x
                    else:
                        dice1.velocity.y, dice2.velocity.y = -dice1.velocity.y, -dice2.velocity.y

    def clear_dice(self):
        """Removes all dice objects from the dice group, effectively clearing the screen of dice"""
        self.dice_timer = -1
        for group in self.sprite_groups:
            for sprite in group:
                sprite.kill()

    def process_data(self, data: list[Any]):
        """
        Processes a list of data and spawns dice according to the provided data.

        Parameters:
        - data (list[Any]): A list of data to be processed. The data should correspond to the fields in the DataModel class.
        """
        data_dict = {key: value for key, value in zip(DataModel.model_fields.keys(), data)}
        self.spawn_dice(**data_dict)

    def load_image_file(self, image_file: str) -> bool:
        """Loads an image from file into the projector.

        Args:
            image_file (str): The file path of the image to be loaded.

        Returns:
            bool: True if successful, False if unsuccessful
        """
        try:
            self.image = pygame.image.load(image_file)
            self.blit()
            self.set_current_image(os.path.basename(image_file))
            return True
        except:
            return False

    def load_image_pil(self, image_pil: Image.Image) -> bool:
        """Loads a PIL Image object into the projector.

        Args:
            image_pil (Image.Image): The object being loaded

        Returns:
            bool: True if successful, False if unsuccessful
        """
        try:
            image_data = image_pil.tobytes()  # type: ignore[reportUnknownMemberType]
            self.image = pygame.image.frombuffer(image_data, image_pil.size, image_pil.mode)  # type: ignore[reportArgumentType]
            self.blit()
            self.set_current_image("hexmap")
            return True
        except:
            return False

    def set_current_image(self, image_name: str):
        """Set the name of the current image loaded"""
        self.current_image = image_name

    def get_current_image(self, max_length: int = 15) -> str:
        """Get the name of the current image loaded"""
        file_name = os.path.basename(self.current_image)
        if len(file_name) > max_length:
            return file_name[:max_length] + "..."
        return file_name

    def get_image_pil(self) -> Image.Image:
        """Get PIL image object from pygame display"""
        bytes_data = pygame.image.tostring(self.image, "RGBA")
        image_pil = Image.frombytes("RGBA", self.image.get_size(), bytes_data)  # type: ignore[reportUnknownMemberType]
        return image_pil

    def update_resolution(self, resolution: Coordinate):
        """Updates the screen resolution."""
        self.resolution = resolution
        os.environ["SDL_VIDEO_CENTERED"] = "1"
        self.screen = pygame.display.set_mode(self.resolution(), flags=pygame.NOFRAME, display=self.display)

    def blit(self):
        """Blits the loaded image onto the screen. Auto-sizes image depending on screen resolution."""
        self.screen.fill((0, 0, 0))
        sw, sh = self.resolution()
        iw, ih = self.image.get_width(), self.image.get_height()
        if iw / ih > sw / sh:
            t = sw / iw
        else:
            t = sh / ih
        self.image = pygame.transform.scale(self.image, (t * iw, t * ih))
        self.screen.blit(self.image, ((sw - t * iw) / 2, (sh - t * ih) / 2))
        self.draw_dice()

    def update(self):
        """Update pygame display"""
        self.update_dice()
        self.blit()
        pygame.display.update()
