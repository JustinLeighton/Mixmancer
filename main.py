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
from PIL import Image, ImageTk
from tkinter import ttk
import os
import pygame

from mixmancer.config.settings import LoadSettings

from mixmancer.gui.popup import ImagePopup, MusicPopup, SfxPopup
from mixmancer.gui.button import CustomButton

from mixmancer.display.image import ImageProjector


class gui(tk.Tk):
    def __init__(self):
        super().__init__()
        self.settings = LoadSettings()
        self.title('Mixmancer')
        self.geometry('400x400')
        self.configure(background='#36393f')
        pygame.mixer.init()
        pygame.init()
        self.projector = ImageProjector(self.settings)
        self.hexmap = None

        # Image button
        self.image_button = ttk.Button(self, text='Select Image', command=self.open_image_popup)
        self.image_button.grid(row=0, column=0, padx=10, pady=5)
        self.selected_image_label = ttk.Label(self, text='Selected Image:')
        self.selected_image_label.grid(row=0, column=1, padx=10, pady=5)

        # Music button
        self.music_button = ttk.Button(self, text='Select Music', command=self.open_music_popup)
        self.music_button.grid(row=1, column=0, padx=10, pady=5)
        self.selected_music_label = ttk.Label(self, text='Selected Music:')
        self.selected_music_label.grid(row=1, column=1, padx=10, pady=5)

        # Music volume slider
        self.music_volume_label = ttk.Label(self, text='Music Volume:')
        self.music_volume_label.grid(row=2, column=0, padx=10, pady=5)
        self.music_volume_slider = ttk.Scale(self, from_=0, to=1, orient='horizontal', command=self.update_volume)
        self.music_volume_slider.set(0.5)
        self.music_volume_slider.grid(row=2, column=1, padx=10, pady=5)

        # Sfx button
        self.sfx_button = ttk.Button(self, text='Select Sfx', command=self.open_sfx_popup)
        self.sfx_button.grid(row=4, column=0, padx=10, pady=5)

        # Sfx volume slider
        self.sfx_volume_label = ttk.Label(self, text='Sfx Volume:')
        self.sfx_volume_label.grid(row=5, column=0, padx=10, pady=5)
        self.sfx_volume_slider = ttk.Scale(self, from_=0, to=1, orient='horizontal', command=self.set_sfx_volume)
        self.sfx_volume_slider.set(0.5)
        self.sfx_volume_slider.grid(row=5, column=1, padx=10, pady=5)

        # Stop Sfx button
        self.sfx_button = ttk.Button(self, text='Stop Sfx', command=self.stop_sfx_sounds)
        self.sfx_button.grid(row=6, column=0, padx=10, pady=5)

        # Hexmap button
        self.hexmap_button = CustomButton(self, text='Hexploration', command=self.open_hexmap)
        self.hexmap_button.grid(row=7, column=0, padx=10, pady=5)

    def open_image_popup(self):
        def update_selected_image(selected_image):
            image_path = os.path.join('assets/img', selected_image)
            image = Image.open(image_path)
            image.thumbnail((100, 100))
            photo_image = ImageTk.PhotoImage(image)
            self.selected_image_label.config(image=photo_image)
            self.selected_image_label.image = photo_image  # Keep reference to the image to avoid garbage collection
            self.projector.load_image(image_path)
        image_popup = ImagePopup(self, callback=update_selected_image)
        image_popup.grab_set()

    def open_music_popup(self):
        def update_selected_music(selected_music):
            self.selected_music_label.config(text=f'Selected Music: {selected_music}')
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
        print('Stuff!')
        
def main():
    app = gui()
    app.mainloop()

if __name__=='__main__':
    main()