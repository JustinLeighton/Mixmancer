# -*- coding: utf-8 -*-
"""
Created on Thu July 3 15:55:08 2023

@author: Justin Leighton
"""

import pygame
import math

class hexMap():
    def __init__(self, image: str, resolution: tuple, hexSize: int, offset: tuple, start: tuple):
        self.image = pygame.image.load(image)
        self.resolution = [int(x) for x in resolution]
        self.hexSize = int(hexSize)
        self.offset = [int(x) for x in offset]
        self.gridLoc = [int(x) for x in start]
        self.stagger = self.gridLoc[0] % 2 == 0 # True = 1-3-3, False = 3-3-1
        self.sideLength = 2 * ((self.hexSize / 2) / math.tan(math.pi / 3))
        self.update()
        
        
    def debug(self):
        print('\n'.join([
            'Debugging',
            'resolution: ' + ','.join([str(x) for x in self.resolution]),
            'hexSize: ' + str(self.hexSize),
            'offset: ' + ','.join([str(x) for x in self.offset]),
            'grid: ' + ','.join([str(x) for x in self.gridLoc]), 
            'pix: ' + ','.join([str(x) for x in self.pixLoc]),
            'stagger: ' + str(self.stagger),
            'sideLength: ' + str(self.sideLength),
            'frame: ' + ','.join([str(x) for x in self.frame()])
            ]))
        
        
    def gridToPix(self, loc: tuple):
        y = loc[0] * self.sideLength * 1.5 + self.offset[1]
        x = loc[1] * self.hexSize + self.offset[0] - (not self.stagger) * 0.5 * self.hexSize
        return y, x
        
    
    def hexPoints(self):
        x = self.resolution[0] / 2
        y = self.resolution[1] / 2
        pad = 1
        return [
            (x - self.hexSize / 2 - pad, y - self.sideLength / 2 - pad),
            (x, y - self.sideLength  - pad),
            (x + self.hexSize / 2 + pad, y - self.sideLength / 2 - pad),
            (x + self.hexSize / 2 + pad, y + self.sideLength / 2 - pad),
            (x, y + self.sideLength),
            (x - self.hexSize / 2 - pad, y + self.sideLength / 2 - pad),
            (x - self.hexSize / 2 - pad, y - self.sideLength / 2 - pad),
            ]

        
    def update(self):
        self.pixLoc = self.gridToPix(self.gridLoc)
        
        
    def logMovement(self):
        with open('map/history.txt', 'a') as f:
            f.write(f"{','.join([str(x) for x in self.gridLoc])}\n")

    
    def move(self, direction: str):
        if direction in ['l', 'ul', 'ur', 'r', 'dr', 'dl']:
            
            if direction == 'l':
                self.gridLoc[1] -= 1
            if direction == 'r':
                self.gridLoc[1] += 1
            if direction == 'ul':
                self.gridLoc[0] -= 1
                self.gridLoc[1] -= not self.stagger
            if direction == 'ur':
                self.gridLoc[0] -= 1
                self.gridLoc[1] += self.stagger
            if direction == 'dl':
                self.gridLoc[0] += 1
                self.gridLoc[1] -= not self.stagger
            if direction == 'dr':
                self.gridLoc[0] += 1
                self.gridLoc[1] += self.stagger
            if direction[0] in ['u','d']:
                self.stagger = not self.stagger
                
            self.update()
            self.logMovement()
            print('Moving to ', ', '.join([str(x) for x in self.gridLoc]))
        else:
            print('Wrong direction! Try l, ul, ur, r, dr, or dl.')
            
    
    def frame(self):
        x = -self.pixLoc[0] + self.resolution[0] / 2
        y = -self.pixLoc[1] + self.resolution[1] / 2
        return (y, x)
    
    
    def dump(self, surface):
        pygame.image.save(surface, 'map/tmp.png')
        
    
    def blit(self, screen):
        screen.fill((0, 0, 0))
        tmp = pygame.Surface((self.resolution[0], self.resolution[1]))
        tmp.blit(self.image, self.frame())
        screen.blit(tmp, (0, 0))
        pygame.draw.polygon(screen, color=(255, 215, 0), points=self.hexPoints(), width=3)
        pygame.display.update()
        
        