import pygame
import random
from typing import Any

from mixmancer.display.sprite import Spritesheet
from mixmancer.display.utils import resize_image_with_aspect_ratio


class ResultWisp(pygame.sprite.Sprite):
    def __init__(
        self,
        starting_location: tuple[int, int],
        target_location: tuple[int, int],
    ):
        super().__init__()
        self.x = float(starting_location[0])
        self.y = float(starting_location[1])
        self.target_location = target_location
        self.w, self.h = 100, 100
        self.sprite_sheet = Spritesheet("assets/dice/fx/green.png")
        self.sprite_index = 0
        self.end_flag = False
        self.rect = pygame.Rect(int(self.x), int(self.y), self.w, self.h)
        self.rotation = random.randint(0, 360)
        self.dx = (target_location[0] - self.rect.x) / self.sprite_sheet.total_frames
        self.dy = (target_location[1] - self.rect.y) / self.sprite_sheet.total_frames

    def update_position(self):
        self.x += self.dx
        self.y += self.dy
        self.rect = pygame.Rect(int(self.x), int(self.y), self.w, self.h)

    def update(self, *args: Any, **kwargs: Any):
        """Updates the sprite's animation and movement."""
        if not self.rect.colliderect(pygame.Rect(self.target_location[0], self.target_location[1], 10, 10)):
            self.image, self.end_flag = self.sprite_sheet.get_sprite(str(self.sprite_index))
            self.image = pygame.transform.scale(self.image, (self.w, self.h))
            self.image = pygame.transform.rotate(self.image, angle=self.rotation)
            if self.end_flag:
                self.sprite_index = 0
                self.end_flag = False
            else:
                self.sprite_index += 1
            self.update_position()
        else:
            self.image = pygame.Surface((self.w, self.h), pygame.SRCALPHA)
            self.image.fill((255, 0, 0))
            self.end_flag = True


class TextSprite(pygame.sprite.Sprite):
    def __init__(
        self,
        text: str,
        location: tuple[int, int],
        font_name: str = "Arial",
        font_size: int = 30,
        color: tuple[int, int, int] = (255, 255, 255),
        backdrop: bool = True,
        backdrop_image_path: str = "assets/dice/result_backdrop.png",
    ):
        super().__init__()
        self.text = text
        self.location = location
        self.font_name = font_name
        self.font_size = font_size
        self.color = color
        self.font = pygame.font.SysFont(self.font_name, self.font_size)
        self.backdrop = backdrop
        self.backdrop_image_path = backdrop_image_path

        self.backdrop_image: pygame.Surface
        if self.backdrop:
            self.backdrop_image = pygame.image.load(self.backdrop_image_path).convert_alpha()
            self.backdrop_image = resize_image_with_aspect_ratio(self.backdrop_image, width=200)
        else:
            self.backdrop_image = pygame.Surface((0, 0), pygame.SRCALPHA)

        self.update()

    def update(self, *args: Any, **kwargs: Any):

        self.image = self.font.render(self.text, True, self.color)
        self.rect = self.image.get_rect(center=self.location)

        if self.backdrop:
            self.image = pygame.Surface(self.backdrop_image.get_size(), pygame.SRCALPHA)
            self.image.blit(self.backdrop_image, (0, 5))
            text_surface = self.font.render(self.text, True, self.color)
            text_rect = text_surface.get_rect(center=self.backdrop_image.get_rect().center)
            self.image.blit(text_surface, text_rect)
        else:
            text_surface = self.font.render(self.text, True, self.color)
            self.image = pygame.Surface(text_surface.get_size(), pygame.SRCALPHA)
            self.image.blit(text_surface, (0, 0))

        self.rect = self.image.get_rect(center=self.location)
