import tkinter as tk
from PIL import Image, ImageTk
from tkinter import ttk
import os
import pygame


class BasePopup(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)

    def _open_popup(self):
        # Open popup near the mouse cursor
        self.update_idletasks()  # Ensure the window is updated before getting its size
        popup_width = self.winfo_width()
        popup_height = self.winfo_height()
        x, y = self._get_mouse_position()
        self.geometry(f"+{x-popup_width//2}+{y-popup_height//2}")  # Position the popup near the mouse cursor

    def _get_mouse_position(self):
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        mouse_x = self.winfo_pointerx()
        mouse_y = self.winfo_pointery()

        # Adjust position if the mouse is close to the edge of the screen
        x = min(mouse_x, screen_width - self.winfo_width())
        y = min(mouse_y, screen_height - self.winfo_height())
        return x, y


class ImagePopup(BasePopup):
    def __init__(self, master, callback):
        super().__init__(master)
        self.title("Select Image")
        self.callback = callback

        # Load images
        image_dir = "assets/img"
        self.images = []
        for filename in os.listdir(image_dir):
            if filename.endswith(".jpg"):
                try:
                    image_path = os.path.join(image_dir, filename)
                    image = Image.open(image_path)
                    image.thumbnail((50, 50))  # Resize image to fit button
                    self.images.append((filename, ImageTk.PhotoImage(image)))
                except (OSError, IOError, Image.UnidentifiedImageError) as e:
                    print(f"Error loading image '{filename}': {e}")

        # Create buttons for each image
        for i, (filename, image) in enumerate(self.images):
            button = ttk.Button(self, image=image, command=lambda idx=i: self.select_image(idx))
            button.grid(row=i // 3, column=i % 3, padx=5, pady=5)

        # Open popup near the mouse cursor
        self._open_popup()

    def select_image(self, index):
        selected_image = self.images[index][0]
        self.callback(selected_image)
        self.destroy()


class MusicPopup(BasePopup):
    def __init__(self, master, callback, volume_control=None):
        super().__init__(master)
        self.title("Select Music")
        self.callback = callback
        self.volume_control = volume_control
        self.music_dir = "assets/mp3"

        # Load music files
        self.music_files = [filename for filename in os.listdir(self.music_dir) if filename.endswith(".mp3")]

        # Create buttons for each music file
        for i, filename in enumerate(self.music_files):
            button = ttk.Button(self, text=filename, command=lambda idx=i: self.select_music(idx))
            button.grid(row=i, column=0, padx=5, pady=5)
        
        # Open popup near the mouse cursor
        self._open_popup()

    def select_music(self, index):
        selected_music = self.music_files[index]
        self.callback(selected_music)
        pygame.mixer.music.load(os.path.join(self.music_dir, selected_music))
        pygame.mixer.music.play()

        # Adjust volume if volume control function is provided
        if self.volume_control:
            self.volume_control(pygame.mixer.music.get_volume())

        self.destroy()

    def set_volume(self, volume):
        pygame.mixer.music.set_volume(volume)


class SfxPopup(BasePopup):
    def __init__(self, master):
        super().__init__(master)
        self.title("Select Sound Effect")
        self.sound_effects_dir = "assets/sfx"

        # Load sound effects files
        self.sound_effects_files = [filename for filename in os.listdir(self.sound_effects_dir) if filename.endswith(".wav")]

        # Create buttons for each sound effect file
        for i, filename in enumerate(self.sound_effects_files):
            button = ttk.Button(self, text=filename, command=lambda idx=i: self.play_sound_effect(idx))
            button.grid(row=i, column=0, padx=5, pady=5)

        # Open popup near the mouse cursor
        self._open_popup()

    def play_sound_effect(self, index):
        selected_sound_effect = self.sound_effects_files[index]
        sound_effect = pygame.mixer.Sound(os.path.join(self.sound_effects_dir, selected_sound_effect))
        sound_effect.play()
        self.destroy()