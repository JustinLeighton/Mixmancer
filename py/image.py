# -*- coding: utf-8 -*-
"""
Created on Tue Aug  8 22:13:09 2023

@author: Justin Leighton
"""

import pygame
import os

class Image():
    def __init__(self, image_input: str, resolution: tuple):
        self.status = False
        self.resolution = resolution
        image_path = self.check_for_file(image_input)
        if image_path:
            self.status = self.load_image(image_path)
        else:
            self.print_help()
            
    
    def check_for_file(self, file: str) -> str:
        self.files = [x for x in os.listdir('img') if x.split('.')[-1].lower() in ['jpg', 'png']]
        for f in self.files:
            if f.split('.')[0].lower() == file:
                return f
        return ''
    
    
    def load_image(self, image: str) -> bool:
        self.image = pygame.image.load(f'img\{image}')
        return True
    
    
    def get_status(self) -> bool:
        return self.status
    
    
    def print_help(self):
        print('Images currently available:', *set([x.split('.')[0] for x in self.files]), sep='\n\t')
    
    
    def blit(self, screen):
        screen.fill((0, 0, 0))
        sw, sh = self.resolution
        iw, ih = self.image.get_width(), self.image.get_height()
        if iw / ih > sw / sh:
            t = sw / iw
        else:
            t = sh / ih
        self.image = pygame.transform.scale(self.image, (t * iw, t * ih))
        screen.blit(self.image, ((sw - t * iw) / 2, (sh - t * ih) / 2))
        pygame.display.update()