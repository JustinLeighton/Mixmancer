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
from mixmancer.gui.theme import CustomTheme, CustomButton, CustomSlider, CustomLabel, CustomImage, SquareButton
from mixmancer.gui.commands import stop_sfx_sounds, set_music_volume
from mixmancer.display.image import ImageProjector
from mixmancer.display.hexmap import HexMap

class gui(tk.Tk):
    def __init__(self):
        super().__init__()
        self.settings = Settings()
        CustomTheme(self.settings.color)
        self.configure(background=self.settings.color['grey'])
        self.title('Mixmancer')
        self.geometry('500x500')
        pygame.mixer.init()
        pygame.init()
        self.projector = ImageProjector((self.settings.width, self.settings.height), self.settings.display)
        self.hexmap = HexMap('./assets/map/map.png', (self.settings.width, self.settings.height), 56, (-2, -6), (43, 131))
        self.hexmap_flag = False

        # Generate widgets
        widget_configs = [
            {'name': 'image_selection_button', 'widget': CustomButton, 'text': 'Select Image', 'command': self.open_image_popup, 'x': 10, 'y': 10},
            {'name': 'image_selection_label', 'widget': CustomImage, 'x': 150, 'y': 10},
            {'name': 'music_selection_button', 'widget': CustomButton, 'text': 'Select Music', 'command': self.open_music_popup, 'x': 10, 'y': 50},
            {'name': 'music_selection_label', 'widget': CustomLabel, 'text': 'Selected Music', 'x': 10, 'y': 90},
            {'name': 'music_volume_slider', 'widget': CustomSlider, 'from_': 0, 'to': 1, 'orient': 'horizontal', 'command': set_music_volume, 'x': 10, 'y': 130},
            {'name': 'sfx_selection_button', 'widget': CustomButton, 'text': 'Select Sfx', 'command': self.open_sfx_popup, 'x': 10, 'y': 170},
            {'name': 'sfx_volume_slider', 'widget': CustomSlider, 'from_': 0, 'to': 1, 'orient': 'horizontal', 'command': self.set_sfx_volume, 'x': 10, 'y': 210},
            {'name': 'sfx_stop_button', 'widget': CustomButton, 'text': 'Stop Sfx', 'command': stop_sfx_sounds, 'x': 10, 'y': 250},
            {'name': 'hexploration_activation_button', 'widget': CustomButton, 'text': 'Hexploration', 'command': self.open_hexmap, 'x': 10, 'y': 290}
        ]

        # Create widgets dynamically
        self.widgets = {}  # Dictionary to store references to created widgets
        for config in widget_configs:
            widget_class = config.pop('widget')
            name = config.pop('name')
            kwargs = {key: value for key, value in config.items()}
            widget = widget_class(self, **kwargs)
            widget.place(x=config['x'], y=config['y'])
            self.widgets[name] = widget  # Store reference to the widget

        # Hexmap movement buttons
        button_info = [
            ('Upper Right', (10, 200)), 
            ('Upper Left', (20, 200)), 
            ('Right', (30, 200)), 
            ('Left', (40, 200)), 
            ('Lower Right', (50, 200)), 
            ('Lower Left', (60, 200)),
            ('Undo', (70, 200)),
            ('History', (80, 200)),
            ('Fog', (90, 200))
        ]
        self.hexmap_buttons = []
        for text, location in button_info:
            button = SquareButton(self, image=f'assets/app/{text}.png', color=self.settings.color, command=lambda btn=text: self.command_hexmap(btn))
            self.hexmap_buttons.append((button, location))

    def update_selected_image(self, selected_image):
        image_path = os.path.join('assets/img', selected_image)
        self.projector.load_image(image_path)
        image = Image.open(image_path)
        image.thumbnail((100, 100))
        photo_image = ImageTk.PhotoImage(image)
        self.widgets['image_selection_label'].config(image=photo_image)
        self.widgets['image_selection_label'].image = photo_image

    def open_image_popup(self):
        image_popup = ImagePopup(self, callback=self.update_selected_image)
        image_popup.grab_set()
        if self.hexmap_flag:
            self.toggle_hexmap_controls()

    def open_music_popup(self):
        def update_selected_music(selected_music):
            self.widgets['music_selection_label'].config(text=selected_music)
        music_popup = MusicPopup(self, callback=update_selected_music)
        music_popup.grab_set()

    def open_sfx_popup(self):
        sfx_popup = SfxPopup(self, self.sfx_volume)
        sfx_popup.grab_set()

    def open_hexmap(self):
        if not self.hexmap_flag:
            self.display_hexmap()
            self.toggle_hexmap_controls()

    def display_hexmap(self):
        image_path = self.hexmap.dump()
        self.projector.load_image(image_path)
        image = Image.open(image_path)
        image.thumbnail((100, 100))
        photo_image = ImageTk.PhotoImage(image)
        self.widgets['image_selection_label'].config(image=photo_image)
        self.widgets['image_selection_label'].image = photo_image

    def toggle_hexmap_controls(self):
        if self.hexmap_flag:
            self.hexmap_flag = False
            for button, _ in self.hexmap_buttons:
                button.place_forget()
        else:
            self.hexmap_flag = True
            for button, location in self.hexmap_buttons:
                button.place(x=location[0], y=location[1])
    
    def command_hexmap(self, direction: str):
        self.hexmap.command(direction)
        self.display_hexmap()
    
        
def main():
    app = gui()
    app.mainloop()

if __name__=='__main__':
    main()