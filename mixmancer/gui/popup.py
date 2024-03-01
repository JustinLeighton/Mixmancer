import tkinter as tk
from PIL import Image, ImageTk
from tkinter import ttk
import os
import pygame


class BasePopup(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)

    def on_mouse_wheel(self, event):
        self.yview_scroll(-1 * (event.delta // 120), "units")

    def _open_popup(self):
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

    def make_scrollable(self, widget):
        canvas = tk.Canvas(self)
        scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL, command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Bind mouse wheel event to the canvas
        canvas.bind_all("<MouseWheel>", lambda event: canvas.yview_scroll(-1 * (event.delta // 120), "units"))

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        return scrollable_frame


class ImagePopup(BasePopup):
    def __init__(self, master, callback, width=500, height=300):
        super().__init__(master)
        self.title("Select Image")
        self.callback = callback
        self.geometry(f"{width}x{height}")

        # Load images
        image_dir = "assets/img"
        self.images = []
        for filename in os.listdir(image_dir):
            if filename.endswith(".jpg"):
                try:
                    image_path = os.path.join(image_dir, filename)
                    image = Image.open(image_path)
                    image.thumbnail((100, 100))  # Resize image to fit button
                    self.images.append((filename, ImageTk.PhotoImage(image)))
                except (OSError, IOError, Image.UnidentifiedImageError) as e:
                    print(f"Error loading image '{filename}': {e}")

        # Create buttons for each image
        scrollable_frame = self.make_scrollable(self)
        for i, (filename, image) in enumerate(self.images):
            button = ttk.Button(scrollable_frame, image=image, command=lambda idx=i: self.select_image(idx))
            button.grid(row=i // 4, column=i % 4, padx=5, pady=5)

        # Open popup near the mouse cursor
        self._open_popup()

    def select_image(self, index):
        selected_image = self.images[index][0]
        self.callback(selected_image)
        self.destroy()


class MusicPopup(BasePopup):
    def __init__(self, master, callback):
        super().__init__(master)
        self.title("Select Music")
        self.callback = callback
        self.music_dir = "assets/mp3"

        # Load music files
        self.music_files = [filename for filename in os.listdir(self.music_dir) if filename.endswith(".mp3")]

        # Create buttons for each music file
        for i, filename in enumerate(self.music_files):
            button = ttk.Button(self, text=filename, command=lambda idx=i: self.select_music(idx))
            button.grid(row=i, column=0, padx=5, pady=5)

        # Open popup near the mouse cursor
        return self._open_popup()

    def select_music(self, index):
        selected_music = self.music_files[index]
        self.callback(selected_music)
        pygame.mixer.music.load(os.path.join(self.music_dir, selected_music))
        pygame.mixer.music.play()

        self.destroy()

    def set_volume(self, volume):
        pygame.mixer.music.set_volume(volume)


class SfxPopup(BasePopup):
    def __init__(self, master, volume):
        super().__init__(master)
        self.title("Select Sound Effect")
        self.sound_effects_dir = "assets/sfx"

        # Load sound effects files
        self.sound_effects_files = [filename for filename in os.listdir(self.sound_effects_dir) if filename.endswith(".wav")]

        # Create buttons for each sound effect file
        for i, filename in enumerate(self.sound_effects_files):
            button = ttk.Button(self, text=filename, command=lambda idx=i: self.play_sound_effect(idx, volume))
            button.grid(row=i, column=0, padx=5, pady=5)

        # Open popup near the mouse cursor
        self._open_popup()

    def play_sound_effect(self, index, volume):
        selected_sound_effect = self.sound_effects_files[index]
        sound_effect = pygame.mixer.Sound(os.path.join(self.sound_effects_dir, selected_sound_effect))
        sound_effect.set_volume(volume)
        sound_effect.play()
        self.destroy()
