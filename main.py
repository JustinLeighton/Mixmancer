# -*- coding: utf-8 -*-
'''
Created on Thu May 18 23:31:42 2023

@author: Justin Leighton
'''

# import pygame
# from mixmancer.display.hexmap import generate_hexMap
# from mixmancer.display.image import image_manager
# from mixmancer.music.music import music_manager
# from mixmancer.config.settings import load_settings, print_menu

import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import os
import pygame

from mixmancer.config.settings import Settings

from mixmancer.gui.popup import ImagePopup, MusicPopup, SfxPopup
from mixmancer.gui.theme import CustomTheme, CustomButton, CustomSlider, CustomLabel, CustomImage

from mixmancer.display.image import ImageProjector
from mixmancer.display.hexmap import HexMap

class gui(tk.Tk):
    def __init__(self):
        super().__init__()
        self.settings = Settings()
        CustomTheme(self.settings.color)
        self.configure(background=self.settings.color['grey'])
        self.title('Mixmancer')
        self.geometry('400x400')
        pygame.mixer.init()
        pygame.init()
        self.projector = ImageProjector((self.settings.width, self.settings.height), self.settings.display)
        self.hexmap = HexMap('./assets/map/map.png', (self.settings.width, self.settings.height), 56, (-2, -6), (43, 131))
        self.hexmap_flag = False

        # Define grid
        self.left_frame = ttk.Frame(self)
        self.left_frame.grid(row=0, column=0, sticky='nsew')
        self.right_frame = ttk.Frame(self)
        self.right_frame.grid(row=0, column=1, sticky='nsew')

        # Image button
        self.image_button = CustomButton(self.left_frame, text='Select Image', command=self.open_image_popup)
        self.image_button.grid(row=0, column=0, padx=10, pady=5)
        self.selected_image_label = CustomImage(self.right_frame)
        self.selected_image_label.grid(row=0, column=1, padx=10, pady=5)

        # Music button
        self.music_button = CustomButton(self.left_frame, text='Select Music', command=self.open_music_popup)
        self.music_button.grid(row=1, column=0, padx=10, pady=5)
        self.selected_music_label = CustomLabel(self.left_frame, text='Selected Music:')
        self.selected_music_label.grid(row=1, column=1, padx=10, pady=5)

        # Music volume slider
        self.music_volume_label = CustomLabel(self.left_frame, text='Music Volume:')
        self.music_volume_label.grid(row=2, column=0, padx=10, pady=5)
        self.music_volume_slider = CustomSlider(self.left_frame, from_=0, to=1, orient='horizontal', command=self.update_volume)
        self.music_volume_slider.set(0.5)
        self.music_volume_slider.grid(row=2, column=1, padx=10, pady=5)

        # Sfx button
        self.sfx_button = CustomButton(self.left_frame, text='Select Sfx', command=self.open_sfx_popup)
        self.sfx_button.grid(row=4, column=0, padx=10, pady=5)

        # Sfx volume slider
        self.sfx_volume_label = CustomLabel(self.left_frame, text='Sfx Volume:')
        self.sfx_volume_label.grid(row=5, column=0, padx=10, pady=5)
        self.sfx_volume_slider = CustomSlider(self.left_frame, from_=0, to=1, orient='horizontal', command=self.set_sfx_volume)
        self.sfx_volume_slider.set(0.5)
        self.sfx_volume_slider.grid(row=5, column=1, padx=10, pady=5)

        # Stop Sfx button
        self.sfx_button = CustomButton(self.left_frame, text='Stop Sfx', command=self.stop_sfx_sounds)
        self.sfx_button.grid(row=6, column=0, padx=10, pady=5)

        # Hexmap button
        self.hexmap_button = CustomButton(self.left_frame, text='Hexploration', command=self.open_hexmap)
        self.hexmap_button.grid(row=7, column=0, padx=10, pady=5)

    def open_image_popup(self):
        self.hexmap_flag = False
        def update_selected_image(selected_image):
            image_path = os.path.join('assets/img', selected_image)
            self.projector.load_image(image_path)
            
            image = Image.open(image_path)
            image.thumbnail((100, 100))
            photo_image = ImageTk.PhotoImage(image)
            self.selected_image_label.config(image=photo_image)
            self.selected_image_label.image = photo_image  # Keep reference to the image to avoid garbage collection

        image_popup = ImagePopup(self, callback=update_selected_image)
        image_popup.grab_set()

    def open_music_popup(self):
        def update_selected_music(selected_music):
            self.selected_music_label.config(text=selected_music)
        music_popup = MusicPopup(self, callback=update_selected_music)
        music_popup.grab_set()
    
    def update_current_music(self, music):
        self.current_music.set(music)

    def update_volume(self, volume):
        self.set_music_volume(float(volume))

    def set_music_volume(self, volume):
        pygame.mixer.music.set_volume(volume) 

    def open_sfx_popup(self):
        sfx_popup = SfxPopup(self, self.sfx_volume)
        sfx_popup.grab_set()

    def set_sfx_volume(self, volume):
        self.sfx_volume = float(volume)

    def stop_sfx_sounds(self):
        pygame.mixer.stop()

    def open_hexmap(self):
        if not self.hexmap_flag:
            image_path = self.hexmap.dump()
            self.projector.load_image(image_path)
            image = Image.open(image_path)
            image.thumbnail((100, 100))
            photo_image = ImageTk.PhotoImage(image)
            self.selected_image_label.config(image=photo_image)
            self.selected_image_label.image = photo_image
            self.hexmap_flag = True
    
        
def main():
    app = gui()
    app.mainloop()

if __name__=='__main__':
    main()