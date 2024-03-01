# -*- coding: utf-8 -*-
"""
Created on Thu July 3 15:55:08 2023

@author: Justin Leighton
"""

import pygame
import math

class generate_hexMap():
    def __init__(self, image: str, resolution: tuple, hexSize: int, offset: tuple, start: tuple):
        self.image = pygame.image.load(image)
        self.resolution = [int(x) for x in resolution]
        self.hexSize = int(hexSize)
        self.offset = [int(x) for x in offset]
        self.gridLoc: list = [int(x) for x in start]
        self.sideLength: float = 2 * ((self.hexSize / 2) / math.tan(math.pi / 3))
        self.update()
        self.fog = False
        self.hist = True
        
        self.yellow = (255, 215, 0)
        
        
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
        x = loc[1] * self.hexSize + self.offset[0] - (not self.checkStagger(loc)) * 0.5 * self.hexSize
        return y, x
    

    def checkStagger(self, loc: tuple):
        return loc[0] % 2 == 0 # True = 1-3-3, False = 3-3-1
        
    
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
        self.stagger = self.checkStagger(self.gridLoc)
        self.pixLoc = self.gridToPix(self.gridLoc)
        
    def logMovement(self):
        with open('map/history.txt', 'a') as f:
            f.write(f"{','.join([str(x) for x in self.gridLoc])}\n")


    def getHexOnScreen(self):
        pass


    def checkOnScreen(self, loc: tuple) -> bool:
        for i in (0,1):
            if loc[i] > self.pixLoc[i] + self.resolution[::-1][i]/2 or loc[i] < self.pixLoc[i] - self.resolution[::-1][i]/2:
                return False
        return True


    def readHist(self): # 23,141
        with open('map/history.txt', 'r') as file:
            data = []
            for line in file:
                try:
                    y, x = map(int, line.strip().split(','))
                    data.append((y, x))
                except ValueError as e:
                    print(f"Error converting line '{line.strip()}' to int: {e}")
        return data


    def getHist(self):
        output = []
        for p in self.readHist():
            p = self.gridToPix(p)
            if self.checkOnScreen(p):
                output.append(p)
        return output
    

    def undoMovement(self):
        data = self.readHist()
        data = data[:-1]
        self.gridLoc = list(data[len(data)-1])
        with open('map/history.txt', 'w') as f:
            f.writelines(','.join(map(str, x)) + '\n' for x in data)
        self.update()
        print('Undoing movement. Going back to', ', '.join([str(x) for x in self.gridLoc]))


    def getFog(self):
        with open('map/history.txt', 'r') as f:
            log = f.read()
        log = log.split('\n')[-10:]
        hexes = self.getHexOnScreen()
        
        # Create adjacent tiles
        clearTiles = set()
        for x in log:
            clearTiles.add(x)
        
        fogTiles = [x for x in hexes if x not in clearTiles]
                
        # Draw fog for each of fogTiles
        for x in fogTiles:
            pass
        

    def normalizePixLoc(self, loc: tuple) -> tuple:
        return tuple(loc[i] - self.pixLoc[i] + self.resolution[::-1][i] / 2 for i in (1, 0))


    def loc(self):
        print('Currently at', ', '.join([str(x) for x in self.gridLoc]))

    
    def move(self, direction: str):
        print(self.gridLoc, type(self.gridLoc))
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

            self.update()
            self.logMovement()
            print('Moving to', ', '.join([str(x) for x in self.gridLoc]))
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
        surf = pygame.Surface((self.resolution[0], self.resolution[1]))
        surf.blit(self.image, self.frame())
        screen.blit(surf, (0, 0))

        # Draw fog
        if self.fog:
            self.drawFog(screen)
        
        # Draw history
        if self.hist:
            history = self.getHist()
            prevPoint = None
            for p in history:
                currentPoint = self.normalizePixLoc(p)
                if prevPoint is not None:
                    pygame.draw.line(screen, self.yellow, prevPoint, currentPoint, 2)
                prevPoint = currentPoint
        
        # Draw current location
        pygame.draw.polygon(screen, color=self.yellow, points=self.hexPoints(), width=3)

        # Update display
        pygame.display.update()
        
        