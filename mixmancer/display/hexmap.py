# -*- coding: utf-8 -*-
"""
Created on Thu July 3 15:55:08 2023

@author: Justin Leighton
"""

import pygame
import math

class HexMap():
    def __init__(self, image_path: str, resolution: tuple, hex_size: int, offset: tuple, start: tuple):
        self.image = pygame.image.load(image_path)
        self.resolution = [int(x) for x in resolution]
        self.hex_size = int(hex_size)
        self.offset = [int(x) for x in offset]
        self.location_grid: list = [int(x) for x in start]
        self.side_length: float = 2 * ((self.hex_size / 2) / math.tan(math.pi / 3))
        self.update()
        self.fog = False
        self.hist = False
        self.yellow = (255, 215, 0)
    
    def update(self):
        self.stagger = self.check_stagger(self.location_grid)
        self.location_pixel = self.grid_to_pixel(self.location_grid)

    def check_stagger(self, grid_location: tuple):
        return grid_location[0] % 2 == 0 # True = 1-3-3, False = 3-3-1

    def frame(self):
        x = -self.location_pixel[0] + self.resolution[0] / 2
        y = -self.location_pixel[1] + self.resolution[1] / 2
        return (y, x)

    def grid_to_pixel(self, grid_location: tuple):
        y = grid_location[0] * self.side_length * 1.5 + self.offset[1]
        x = grid_location[1] * self.hex_size + self.offset[0] - (not self.check_stagger(grid_location)) * 0.5 * self.hex_size
        return y, x

    def hex_points(self):
        x = self.resolution[0] / 2
        y = self.resolution[1] / 2
        pad = 1
        return [
            (x - self.hex_size / 2 - pad, y - self.side_length / 2 - pad),
            (x, y - self.side_length  - pad),
            (x + self.hex_size / 2 + pad, y - self.side_length / 2 - pad),
            (x + self.hex_size / 2 + pad, y + self.side_length / 2 - pad),
            (x, y + self.side_length),
            (x - self.hex_size / 2 - pad, y + self.side_length / 2 - pad),
            (x - self.hex_size / 2 - pad, y - self.side_length / 2 - pad),
            ]

    def check_on_screen(self, loc: tuple) -> bool:
        for i in (0,1):
            if loc[i] > self.location_pixel[i] + self.resolution[::-1][i]/2 or loc[i] < self.location_pixel[i] - self.resolution[::-1][i]/2:
                return False
        return True

    def normalize_pixel_location(self, loc: tuple) -> tuple:
        return tuple(loc[i] - self.location_pixel[i] + self.resolution[::-1][i] / 2 for i in (1, 0))

    def get_history(self):
        output = []
        for p in self.read_history():
            p = self.grid_to_pixel(p)
            if self.check_on_screen(p):
                output.append(p)
        return output

    def read_hist(self): # 23,141
        with open('./assets/map/history.txt', 'r') as file:
            data = []
            for line in file:
                try:
                    y, x = map(int, line.strip().split(','))
                    data.append((y, x))
                except ValueError as e:
                    print(f"Error converting line '{line.strip()}' to int: {e}")
        return data

    def undo_movement(self):
        data = self.read_history()
        data = data[:-1]
        self.location_grid = list(data[len(data)-1])
        with open('map/history.txt', 'w') as f:
            f.writelines(','.join(map(str, x)) + '\n' for x in data)
        self.update()

    def log_movement(self):
        with open('./assets/map/history.txt', 'a') as f:
            f.write(f"{','.join([str(x) for x in self.gridLoc])}\n")

    def move(self, direction: str):
        if direction in ['l', 'ul', 'ur', 'r', 'dr', 'dl']:
            if direction == 'l':
                self.location_grid[1] -= 1
            if direction == 'r':
                self.location_grid[1] += 1
            if direction == 'ul':
                self.location_grid[0] -= 1
                self.location_grid[1] -= not self.stagger
            if direction == 'ur':
                self.location_grid[0] -= 1
                self.location_grid[1] += self.stagger
            if direction == 'dl':
                self.location_grid[0] += 1
                self.location_grid[1] -= not self.stagger
            if direction == 'dr':
                self.location_grid[0] += 1
                self.location_grid[1] += self.stagger

            self.update()
            self.logMovement()
            print('Moving to', ', '.join([str(x) for x in self.gridLoc]))
        else:
            print('Wrong direction! Try l, ul, ur, r, dr, or dl.')

    def dump(self):
        temp_file = './assets/map/tmp.png'
        surface = pygame.Surface((self.resolution[0], self.resolution[1]))
        surface.fill((0, 0, 0))
        surface.blit(self.image, self.frame())

        # Draw current location
        pygame.draw.polygon(surface, color=self.yellow, points=self.hex_points(), width=3)

        pygame.image.save(surface, temp_file)
        return temp_file
        