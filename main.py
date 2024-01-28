# -*- coding: utf-8 -*-
"""
Created on Thu May 18 23:31:42 2023

@author: Justin Leighton
"""

import pygame
from mixmancer.hexmap import generate_hexMap
from mixmancer.music import music_manager
from mixmancer.image import image_manager
from mixmancer.config import load_settings, print_menu

def main():
    
    # Load settings
    settings = load_settings()

    # Initialize screen
    pygame.init()
    resolution = (settings['WIDTH'], settings['HEIGHT'])
    screen = pygame.display.set_mode(resolution, flags=pygame.NOFRAME, display=settings['DISPLAY'])

    # Initialize music manager
    Music = music_manager()

    # Initialize hexmap placeholder
    hexMap = None

    # Event loop
    running = True; user_input='map'
    while running:

        
        # Exit condition
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False


        # Exit command
        if user_input == 'exit':
            running = False
            

        # Hexploration commands
        elif user_input == 'map':
            with open('map/history.txt', 'r') as f:
                for line in f:
                    pass
                start = line.split(',')
            hexMap = generate_hexMap('map/map.png', resolution, 56, (-2, -6), start)
            hexMap.blit(screen)
            
            
        # Hexploration movement
        elif user_input in ['l', 'ul', 'ur', 'r', 'dr', 'dl'] and hexMap is not None:
            hexMap.move(user_input)
            hexMap.blit(screen)
            

        # Undo movement on hex map
        elif user_input == 'undo' and hexMap is not None:
            hexMap.undoMovement()
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

        
        # Change volume
        elif user_input[:3].lower() == 'vol':
            Music.setVolume(user_input.split(' ')[-1])


        # Change music timestamp
        elif user_input[:4].lower() == 'skip':
            Music.setTimestamp(user_input.split(' ')[-1]) 
            
       
        # Change image
        elif user_input[:4].lower() == 'show':
            Image = image_manager(user_input.split(' ')[-1], resolution)
            if Image.get_status():
                hexMap = None
                Image.blit(screen)
            
        
        # Display command information
        else:
            print_menu()

        # Prompt next user input
        if running:
            user_input = input('Next scene:')

    # Quit Pygame
    pygame.quit()


if __name__=='__main__':
    main() 