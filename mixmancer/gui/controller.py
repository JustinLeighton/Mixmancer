import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from typing import Any

from mixmancer.display.image import ImageProjector
from mixmancer.display.hexmap import HexMap
from mixmancer.sound.mixer import Mixer
from mixmancer.gui.theme import CustomTheme
from mixmancer.config.settings import (
    get_projector_resolution,
    get_hexmap_size,
    get_hexmap_offset,
    get_hexmap_start,
)


class Controller(tk.Tk):
    """Main controller for tkinter frames"""

    def __init__(self):
        super().__init__()
        self.configure_theme()
        self.settings_path = "mixmancer/config/settings.json"
        self.hexmap_path = "assets/map/map.png"

        self.container = ttk.Frame(self, style="Custom.TFrame")
        self.container.pack(fill=tk.BOTH, expand=True)
        self.frames: dict[type[ttk.Frame], ttk.Frame] = {}
        self.active_frame: type[ttk.Frame]
        self.image_projector = ImageProjector(get_projector_resolution(), 1)
        self.hexmap = HexMap(
            image_path=self.hexmap_path,
            resolution=get_projector_resolution(),
            hex_size=get_hexmap_size(),
            offset=get_hexmap_offset(),
            start_coordinates=get_hexmap_start(),
        )
        self.image_preview: ImageTk.PhotoImage = None  # type: ignore[reportAttributeAccessIssue]
        self.sfx_volume: float = 0.5
        self.mixer = Mixer()
        self.hexmap_flag = False
        self.theme = CustomTheme()
        self.image_thumbnail_dimensions: tuple[int, int] = (100, 100)

    def show_frame(self, container: type[ttk.Frame]):
        """Display input frame within app window"""
        for frame in self.frames.values():
            frame.place_forget()
        self.frames[container].place(relx=0, rely=0, relwidth=1, relheight=1)
        self.frames[container].update()
        self.active_frame = container

    def configure_theme(self):
        """Configure theme for all frames"""
        style = ttk.Style()
        style.configure("Custom.TFrame", background="lightblue", foreground="black")  # type: ignore[reportUnknownMemberType]

    def load_image_file(self, image_path: str):
        """Displays image on second display and image preview"""
        self.image_projector.load_image_file(image_path)
        self.image_pil = Image.open(image_path)
        self.update_thumnail_image()

    def display_image_file(self, image_path: str):
        """Displays image on second display and image preview"""
        self.load_image_file(image_path)
        if self.hexmap_flag:
            self.hexmap_flag = False

    def update_thumnail_image(self):
        """Display image preview in main app window"""
        self.image_pil = self.image_projector.get_image_pil()
        self.image_pil.thumbnail(self.image_thumbnail_dimensions)
        self.image_preview = ImageTk.PhotoImage(self.image_pil)

    def display_hexmap(self):
        """Display hexmap image"""
        self.image_pil = self.hexmap.get_current_surface_PIL()
        self.image_projector.load_image_pil(self.image_pil)
        self.update_thumnail_image()
        self.hexmap_flag = True
        self.update()

    def update(self):
        """Updates tkinter window"""
        super().update()
        self.frames[self.active_frame].update()
        self.image_projector.update()

    def hexmap_controls(self, command: str):
        """Route hexmap object commands"""
        self.hexmap.command(command)
        self.display_hexmap()

    def update_settings(self):
        print("Did a thing...")

    def process_data(self, data: list[Any]):
        self.image_projector.process_data(data)
