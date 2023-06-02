# -*- coding: utf-8 -*-
"""
Created on Thu May 18 23:31:42 2023

@author: Justin Leighton
"""

import os
import pygame
from pygame import mixer
import pandas as pd

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
    

# Scene change function
def set_scene(df, user_input='main', previous_scene='main'):

    # Load path information
    subset = df[df['scene']==user_input.lower()]
    if subset.shape[0]>0:
        scene = user_input
        image_path = './img/' + subset['image'].iloc[0] if subset['image'].iloc[0] != '' else ''
        music_path = './mp3/' + subset['music'].iloc[0] if subset['music'].iloc[0] != '' else ''
    else:
        scene = 'help'
        subset = df[df['scene']=='main']
        image_path = ''
        music_path = ''

    # Output
    return scene, image_path, music_path

# Music playing function
def play_music(music_path):
    mixer.music.stop()
    mixer.music.unload()
    if music_path!='':
        mixer.music.load(music_path)
        mixer.music.play(-1)

# Load image function
def load_image(image_path, screen):
    sw, sh = pygame.display.get_surface().get_size()
    image = pygame.image.load(image_path)
    iw, ih = image.get_width(), image.get_height()
    if iw/ih > sw/sh:
        t = sw / iw
    else:
        t = sh / ih
    image = pygame.transform.scale(image, (t * iw, t * ih))
    screen.blit(image, ((sw - t * iw)/2, (sh - t * ih)/2))

def main():
    
    # Load settings
    settings = load_settings()

    # Initialize Screen
    pygame.init()
    screen_width, screen_height = 1200, 800
    screen = pygame.display.set_mode((settings['WIDTH'], settings['HEIGHT']), flags=pygame.NOFRAME, display=settings['DISPLAY'])

    # Initialize Music
    mixer.init()

    # Initialize font
    font = pygame.font.SysFont(None, 24)

    # Load scene data
    df = pd.read_csv('db.txt',sep='\t').fillna('')

    # Run the event loop to keep the window open
    running = True; user_input=''; current_song=''
    scene, image, music = set_scene(df)
    while running:

        # Exit condition
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if user_input=='exit':
            running=False
        else: 
            if scene=='help':
                print(df)
            else:
                # Display image
                screen.fill((0,0,0))
                if image!='':
                    load_image(image, screen)

                # Play music
                if music != current_song:
                    play_music(music)
                    current_song = music
                
                # Debug - TEMP!!!
                text = font.render(scene, True, (0,0,0))
                screen.blit(text, (20, 20))

                # Update display
                pygame.display.update()

            # Prompt next user input
            user_input = input('Next scene:')
            scene, image, music = set_scene(df, user_input, scene)

    # Quit Pygame
    pygame.quit()

if __name__=='__main__':
    main() 