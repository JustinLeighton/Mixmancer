# -*- coding: utf-8 -*-
"""
Created on Thu May 18 23:31:42 2023

@author: Justin Leighton
"""

import pygame
from pygame import mixer
import pandas as pd


import sys
sys.path.insert(1, './py')
import hexmap
import music
import image


# Load settings from file
def load_settings():
    with open('settings.txt') as f:
        settings = f.read()
    settings = settings.split('\n')
    d = {}
    for i in settings:
        pair = i.split('=')
        d[pair[0]]=int(pair[1])
    return d


def main():
    
    # Load settings
    settings = load_settings()

    # Initialize Screen
    pygame.init()
    resolution = (settings['WIDTH'], settings['HEIGHT'])
    screen = pygame.display.set_mode(resolution, flags=pygame.NOFRAME, display=settings['DISPLAY'])

    # Initialize Music
    Music = music.Music()

    # Initialize hexmap
    hexMap = None

    # Run the event loop to keep the window open
    running = True; user_input='map'
    while running:

        
        # Exit condition
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False


        # Exit command
        if user_input == 'exit':
            running = False
            
            
        # Display command information
        elif user_input == 'help':
            print('''
            So here's the deal...
            
            map\t\tDisplays hex map
            \t\tInput "l", "ul", "ur", "r", "dr", "dl" to move on the map
            \t\tInput "loc" for output of current grid location
            \t\tInput "debug" for debug output
            play *\tSets track to *. use "help" for * to get options
            show *\tDisplays image to *. use "help" for * to get options
            help\tFor help output, you just did this to get here...
            exit\tExits mixmancer
            ''')
            

        # Enter hexploration
        elif user_input == 'map':
            with open('map/history.txt', 'r') as f:
                for line in f:
                    pass
                start = line.split(',')
            hexMap = hexmap.hexMap('map/map.png', resolution, 56, (-2, -6), start)
            hexMap.blit(screen)
            
            
        # Move on hex map
        elif user_input in ['l', 'ul', 'ur', 'r', 'dr', 'dl'] and hexMap is not None:
            hexMap.move(user_input)
            hexMap.blit(screen)
            
         
        # Debug hex map
        elif user_input == 'debug' and hexMap is not None:
            hexMap.debug()
            
        
        # Show current location
        elif user_input == 'loc' and hexMap is not None:
            hexMap.loc()
        
        
        # Change track
        elif user_input[:4].lower() == 'play':
           Music.play(user_input.split(' ')[-1])
            
       
        # Change image
        elif user_input[:4].lower() == 'show':
            Image = image.Image(user_input.split(' ')[-1], resolution)
            if Image.get_status():
                hexMap = None
                Image.blit(screen)
            
        
        # Display command information
        else:
            print('''
            So here's the deal...
            
            map\t\tDisplays hex map
            \t\tInput "l", "ul", "ur", "r", "dr", "dl" to move on the map
            \t\tInput "loc" for output of current grid location
            \t\tInput "debug" for debug output
            play *\tSets track to *. use "help" for * to get options
            show *\tDisplays image to *. use "help" for * to get options
            help\tFor help output. You just did this to get here, or you're really struggling...
            exit\tExits mixmancer
            ''')

        # Prompt next user input
        if running:
            user_input = input('Next scene:')

    # Quit Pygame
    pygame.quit()


if __name__=='__main__':
    main() 