# -*- coding: utf-8 -*-
"""
Created on Thu May 18 23:31:42 2023

@author: Justin Leighton
"""

# import pygame
# from mixmancer.display.hexmap import generate_hexMap
# from mixmancer.display.image import image_manager
# from mixmancer.music.music import music_manager
# from mixmancer.config.settings import load_settings, print_menu

import tkinter as tk
from PIL import Image, ImageTk
from tkinter import ttk
import os
import pygame

from mixmancer.config.settings import LoadSettings
from mixmancer.gui.popup import ImagePopup, MusicPopup, SfxPopup
from mixmancer.display.image import ImageProjector

class gui(tk.Tk):
    def __init__(self):
        super().__init__()
        self.settings = LoadSettings()
        self.title('Mixmancer')
        self.geometry('400x400')
        pygame.mixer.init()
        pygame.init()
        self.projector = ImageProjector(self.settings)

        # Image button
        self.image_button = ttk.Button(self, text="Select Image", command=self.open_image_popup)
        self.image_button.grid(row=0, column=0, padx=10, pady=5)
        self.selected_image_label = ttk.Label(self, text="Selected Image:")
        self.selected_image_label.grid(row=0, column=1, padx=10, pady=5)

        # Music button
        self.music_button = ttk.Button(self, text="Select Music", command=self.open_music_popup)
        self.music_button.grid(row=1, column=0, padx=10, pady=5)
        self.selected_music_label = ttk.Label(self, text="Selected Music:")
        self.selected_music_label.grid(row=1, column=1, padx=10, pady=5)

        # Music volume slider
        self.music_volume_label = ttk.Label(self, text="Music Volume:")
        self.music_volume_label.grid(row=2, column=0, padx=10, pady=5)
        self.music_volume_slider = ttk.Scale(self, from_=0, to=1, orient="horizontal", command=self.update_volume)
        self.music_volume_slider.set(0.5)  # Default volume
        self.music_volume_slider.grid(row=2, column=1, padx=10, pady=5)

        # Sfx button
        self.sound_effects_button = ttk.Button(self, text="Select Sound Effect", command=self.open_sound_effects_popup)
        self.sound_effects_button.grid(row=2, column=0, padx=10, pady=5)

        # Sfx volume slider
        self.sound_effects_volume_label = ttk.Label(self, text="Sound Effects Volume:")
        self.sound_effects_volume_label.grid(row=4, column=0, padx=10, pady=5)
        self.sound_effects_volume_slider = ttk.Scale(self, from_=0, to=100, orient="horizontal")
        self.sound_effects_volume_slider.grid(row=4, column=1, padx=10, pady=5)

    def open_image_popup(self):
        def update_selected_image(selected_image):
            image_path = os.path.join("assets/img", selected_image)
            image = Image.open(image_path)
            image.thumbnail((50, 50))  # Resize image to fit label
            photo_image = ImageTk.PhotoImage(image)
            self.selected_image_label.config(image=photo_image)
            self.selected_image_label.image = photo_image  # Keep reference to the image to avoid garbage collection
            self.projector.load_image(image_path)

        image_popup = ImagePopup(self, callback=update_selected_image)
        image_popup.grab_set()

    def open_music_popup(self):
        def update_selected_music(selected_music):
            self.selected_music_label.config(text=f"Selected Music: {selected_music}")

        music_popup = MusicPopup(self, callback=update_selected_music)
        music_popup.grab_set()
    
    def update_current_music(self, music):
        self.current_music.set(music)

    def update_volume(self, volume):
        self.set_music_volume(float(volume))

    def set_music_volume(self, volume):
        pygame.mixer.music.set_volume(volume)        

    def open_sound_effects_popup(self):
        sound_effects_popup = SfxPopup(self)
        sound_effects_popup.grab_set()

def main():
    app = gui()
    app.mainloop()


# def main_old():
    
#     # Load settings
#     settings = load_settings()

#     # Initialize screen
#     pygame.init()
#     resolution = (settings['WIDTH'], settings['HEIGHT'])
#     screen = pygame.display.set_mode(resolution, flags=pygame.NOFRAME, display=settings['DISPLAY'])

#     # Initialize music manager
#     Music = music_manager()

#     # Initialize hexmap placeholder
#     hexMap = None

#     # Event loop
#     running = True; user_input='map'
#     while running:

        
#         # Exit condition
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 running = False


#         # Exit command
#         if user_input == 'exit':
#             running = False
            

#         # Hexploration commands
#         elif user_input == 'map':
#             with open('map/history.txt', 'r') as f:
#                 for line in f:
#                     pass
#                 start = line.split(',')
#             hexMap = generate_hexMap('map/map.png', resolution, 56, (-2, -6), start)
#             hexMap.blit(screen)
            
            
#         # Hexploration movement
#         elif user_input in ['l', 'ul', 'ur', 'r', 'dr', 'dl'] and hexMap is not None:
#             hexMap.move(user_input)
#             hexMap.blit(screen)
            

#         # Undo movement on hex map
#         elif user_input == 'undo' and hexMap is not None:
#             hexMap.undoMovement()
#             hexMap.blit(screen)
         
         
#         # Debug hex map
#         elif user_input == 'debug' and hexMap is not None:
#             hexMap.debug()
            
        
#         # Show current location
#         elif user_input == 'loc' and hexMap is not None:
#             hexMap.loc()
        
        
#         # Change track
#         elif user_input[:4].lower() == 'play':
#            Music.play(user_input.split(' ')[-1])

        
#         # Change volume
#         elif user_input[:3].lower() == 'vol':
#             Music.setVolume(user_input.split(' ')[-1])


#         # Change music timestamp
#         elif user_input[:4].lower() == 'skip':
#             Music.setTimestamp(user_input.split(' ')[-1]) 
            
       
#         # Change image
#         elif user_input[:4].lower() == 'show':
#             Image = image_manager(user_input.split(' ')[-1], resolution)
#             if Image.get_status():
#                 hexMap = None
#                 Image.blit(screen)
            
        
#         # Display command information
#         else:
#             print_menu()

#         # Prompt next user input
#         if running:
#             user_input = input('Next scene:')

#     # Quit Pygame
#     pygame.quit()


if __name__=='__main__':
    main() 