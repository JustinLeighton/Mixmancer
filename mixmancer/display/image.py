# -*- coding: utf-8 -*-
"""
Created on Tue Aug  8 22:13:09 2023

@author: Justin Leighton
"""

import pygame

class ImageProjector():
    def __init__(self, settings: dict):
        self.resolution = (settings['WIDTH'], settings['HEIGHT'])
        self.screen = pygame.display.set_mode(self.resolution, flags=pygame.NOFRAME, display=settings['DISPLAY'])
        self.status = False
        self.resolution = self.resolution

    def load_image(self, image: str) -> bool:
        self.image = pygame.image.load(image)
        self.blit()
        return True
    
    def blit(self,):
        self.screen.fill((0, 0, 0))
        sw, sh = self.resolution
        iw, ih = self.image.get_width(), self.image.get_height()
        if iw / ih > sw / sh:
            t = sw / iw
        else:
            t = sh / ih
        self.image = pygame.transform.scale(self.image, (t * iw, t * ih))
        self.screen.blit(self.image, ((sw - t * iw) / 2, (sh - t * ih) / 2))
        pygame.display.update()

