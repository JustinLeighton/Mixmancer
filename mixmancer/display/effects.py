import pygame
import random
from typing import Any

from mixmancer.display.sprite import Spritesheet


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
            self.image = pygame.Surface((self.w, self.h))
            self.image.fill((255, 0, 0))
            self.end_flag = True
