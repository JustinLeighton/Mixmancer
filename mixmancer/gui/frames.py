import tkinter as tk
from tkinter import ttk
import os
from PIL import Image, ImageTk

from typing import Literal, Union

from mixmancer.gui.controller import Controller
from mixmancer.gui.theme import CustomButton, CustomImage, CustomSlider, CustomLabel, SquareButton
from mixmancer.utils import check_file_exists


class StartFrame(ttk.Frame):
    """Starting frame for app. Routes to all other frames."""

    def __init__(self, parent: ttk.Frame, controller: Controller):
        ttk.Frame.__init__(self, parent, style="Custom.TFrame")
        self.controller = controller
        self.grid(row=0, column=0, sticky="nsew")
        self.grid_columnconfigure(0, minsize=150)
        self.grid_columnconfigure(1, weight=1)
        self.left_frame = ttk.Frame(self)
        self.left_frame.grid(row=0, column=0, sticky="nw")
        self.right_frame = ttk.Frame(self)
        self.right_frame.grid(row=0, column=1, sticky="nw")
        self.button_container: dict[str, Union[CustomButton, CustomLabel, CustomSlider, HexMapFrame]] = {}

        # Image selection
        self.button_container["image_selector"] = CustomButton(
            self.left_frame, text="Select Image", command=lambda: controller.show_frame(ImageFrame)
        )

        # Current image selection
        self.button_container["image_selection"] = CustomLabel(self.left_frame, text="")

        # Music selection
        self.button_container["music_selector"] = CustomButton(
            self.left_frame, text="Select Music", command=lambda: controller.show_frame(MusicFrame)
        )

        # Current music selection
        self.button_container["music_selection"] = CustomLabel(self.left_frame, text="")

        # Music volume slider
        self.button_container["music_volume"] = CustomSlider(
            self.left_frame, command=lambda v, c="music": controller.mixer.set_volume(v, c)  # type: ignore[reportUnknownMemberType]
        )

        # Sfx selection
        self.button_container["sfx_selector"] = CustomButton(
            self.left_frame, text="Sound Effects", command=lambda: controller.show_frame(SfxFrame)
        )

        # Sfx volume slider
        self.button_container["sfx_volume"] = CustomSlider(
            self.left_frame, command=lambda v, c="sfx": controller.mixer.set_volume(v, c)  # type: ignore[reportUnknownMemberType]
        )

        # Settings button
        self.button_container["settings_selector"] = CustomButton(
            self.left_frame, text="Settings", command=lambda: controller.show_frame(SettingsFrame)
        )

        # Hexmap button
        self.button_container["hexmap_selector"] = CustomButton(
            self.left_frame, text="Hexmap", command=controller.display_hexmap
        )

        # Hexmap frame
        self.button_container["hexmap_frame"] = HexMapFrame(self.left_frame, self.controller)

        # Place widgets
        for _, widget in self.button_container.items():
            widget.pack(padx=5, pady=5, anchor=tk.NW)

        # Image preview
        self.label_image_preview = CustomImage(self.right_frame)
        self.label_image_preview.pack(anchor=tk.NW, pady=5)
        self.bind("<Configure>", self.resize_preview_image)  # type: ignore

    def update(self):
        """Modify update method to update the configured preview image"""
        super().update()
        if self.controller.image_preview is not None:  # type: ignore[reportUnnecessaryComparison]
            self.controller.update_thumnail_image()
            self.label_image_preview.configure(image=self.controller.image_preview)
        self.button_container["hexmap_frame"].update()

    def resize_preview_image(self, event: Literal[tk.EventType.ResizeRequest]):
        """Resizes preview image on app window when window resizes

        Args:
            event (Literal[tk.EventType.ResizeRequest]): Tkinter window resize event
        """
        if event.widget == self:  # type: ignore[reportUnknownMemberType]
            if self.controller.settings.app_height != event.height or self.controller.settings.app_width != event.width:  # type: ignore[reportUnknownMemberType]
                self.controller.settings.app_height, self.controller.settings.app_width = event.height, event.width  # type: ignore[reportUnknownMemberType]
                self.controller.image_thumbnail_dimensions = self.get_preview_image_size()
                self.update()

    def get_preview_image_size(self, padding: int = 5) -> tuple[int, int]:
        """Get size available for preview image within app window

        REPLACE NUMBERS WITH DYNAMIC REFERENCES"""
        image_width: int = self.controller.settings.app_width - 150 - padding * 2
        image_height: int = self.controller.settings.app_height - 5 - padding * 2
        if image_width < 100 or image_height < 100:
            image_width, image_height = 100, 100
        return image_width, image_height


class ImageFrame(ttk.Frame):
    """Display .jpg/.jpeg/.png files in assets/img for selection"""

    def __init__(self, parent: ttk.Frame, controller: Controller):
        ttk.Frame.__init__(self, parent, style="Custom.TFrame")
        self.controller = controller

        # Create a canvas for scrollable content
        self.canvas = tk.Canvas(self, borderwidth=0)
        self.canvas.pack(side="left", fill="both", expand=True)

        # Add a vertical scrollbar to the canvas
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)  # type: ignore
        self.scrollbar.pack(side="right", fill="y")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.bind_all("<MouseWheel>", self.on_mouse_wheel)  # type: ignore

        # Create a frame inside the canvas to hold the images
        self.inner_frame = ttk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.inner_frame, anchor="nw")
        self.display_image_thumbnails("assets/img")
        self.bind("<Configure>", self.on_configure)  # type: ignore

    def display_image_thumbnails(self, img_dir: str):
        """Displays images found in assets/img in a grid layout for selection"""

        # Check if the directory exists
        if not os.path.exists(img_dir):
            raise FileNotFoundError(f"Directory '{img_dir}' not found.")

        # List all files in the directory
        files = os.listdir(img_dir)
        image_files = [file for file in files if file.lower().endswith((".jpg", ".jpeg", ".png"))]

        # Display thumbnails of each image in a grid pattern
        self.thumbnail_buttons: list[tk.Button] = []
        for image_file in image_files:
            image_path = os.path.join(img_dir, image_file)
            img = Image.open(image_path)
            img.thumbnail((100, 100))
            tk_img = ImageTk.PhotoImage(img)
            btn = tk.Button(
                self.inner_frame, image=tk_img, command=lambda name=image_path: self.thumbnail_selected(name)
            )
            btn.image = tk_img  # type: ignore[reportAttributeAccessIssue]
            self.thumbnail_buttons.append(btn)
        self.layout_thumbnails()

    def layout_thumbnails(self):
        """Dynamically adjusts thumbnail layout based on window width"""
        for widget in self.inner_frame.winfo_children():
            widget.grid_forget()
        width = self.winfo_width()
        num_columns = max(1, width // 120)
        for i, btn in enumerate(self.thumbnail_buttons):
            row = i // num_columns
            column = i % num_columns
            btn.grid(row=row, column=column, padx=5, pady=5)

    def thumbnail_selected(self, image_path: str):
        """Selection function when image is selected"""
        self.controller.display_image_file(image_path)
        self.controller.show_frame(StartFrame)

    def on_mouse_wheel(self, event: Literal[tk.EventType.MouseWheel]):
        """Scrolls frame when called"""
        self.canvas.yview_scroll(-1 * int(event.delta / 120), "units")  # type: ignore[reportUnknownArgumentType]

    def on_configure(self, event: tk.Event):  # type: ignore
        """Configures event functions"""
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        self.layout_thumbnails()


class MusicFrame(ttk.Frame):
    """Display .mp3 files in assets/music for selection"""

    def __init__(self, parent: ttk.Frame, controller: Controller):
        ttk.Frame.__init__(self, parent, style="Custom.TFrame")
        self.controller = controller

        music_dir = "assets/music"
        if os.path.isdir(music_dir):
            mp3_files = [file for file in os.listdir(music_dir) if file.lower().endswith(".mp3")]
            for mp3_file in mp3_files:
                music_file = os.path.join(music_dir, mp3_file)
                button = CustomButton(self, text=mp3_file, command=lambda file=music_file: self.music_selected(file))
                button.pack()

    def music_selected(self, music_file: str):
        """Function to execute when a music file button is selected"""
        self.controller.mixer.play_music(music_file)
        self.controller.show_frame(StartFrame)


class SfxFrame(ttk.Frame):
    """Display wav in assets/sfx files for selection"""

    def __init__(self, parent: ttk.Frame, controller: Controller):
        ttk.Frame.__init__(self, parent, style="Custom.TFrame")
        self.controller = controller

        sfx_dir = "assets/sfx"
        if os.path.isdir(sfx_dir):
            mp3_files = [file for file in os.listdir(sfx_dir) if file.lower().endswith(".wav")]
            for mp3_file in mp3_files:
                sfx_file = os.path.join(sfx_dir, mp3_file)
                button = CustomButton(self, text=mp3_file, command=lambda file=sfx_file: self.sfx_selected(file))
                button.pack()

    def sfx_selected(self, sfx_file: str):
        """Function to execute when a sfx file button is selected"""
        self.controller.mixer.play_sfx(sfx_file)
        self.controller.show_frame(StartFrame)


class HexMapFrame(ttk.Frame):
    """Container for hexmap control buttons"""

    def __init__(self, parent: ttk.Frame, controller: Controller):
        ttk.Frame.__init__(self, parent, style="Custom.TFrame")
        self.controller = controller
        self.parent = parent
        self.visible = False
        self.button_container: dict[str, SquareButton] = {}
        self.button_config: dict[str, tuple[int, int]] = {
            "upper_left": (25, 0),
            "upper_right": (55, 0),
            "left": (10, 30),
            "right": (70, 30),
            "lower_left": (25, 60),
            "lower_right": (55, 60),
            "history": (10, 90),
            "undo": (40, 90),
            "fog": (70, 90),
        }
        for name, coordinates in self.button_config.items():
            image_path = f"assets/app/{name}.png"
            file_exists = check_file_exists(image_path)
            self.button_container[name] = SquareButton(
                self,
                image_path=image_path if file_exists else None,  # type: ignore[reportArgumentType]
                text=None if file_exists else "?",
                coordinates=coordinates,
                command=lambda n=name: self.controller.hexmap_controls(n),  # type: ignore[reportUnknownArgumentType]
            )

    def update(self):
        """Update hexmap frame to hide/show buttons"""
        if not self.visible and not self.controller.hexmap_flag:
            self.hide_buttons()
        elif not self.visible and self.controller.hexmap_flag:
            self.show_buttons()
        super().update()

    def hide_buttons(self):
        """Hide hexmap control buttons"""
        self.visible = False
        for _, btn in self.button_container.items():
            btn.place_forget()

    def show_buttons(self):
        """Show hexmap control buttons"""
        self.visible = True
        for _, btn in self.button_container.items():
            x, y = btn.coordinates
            print(x, y)
            print(btn.winfo_x(), btn.winfo_y())
            print(btn.winfo_rootx(), btn.winfo_rooty())
            btn.pack()
            print("Placed! ---")
            print(x, y)
            print(btn.winfo_x(), btn.winfo_y())
            print(btn.winfo_rootx(), btn.winfo_rooty())
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")


class SettingsFrame(ttk.Frame):
    """Settings menu. Change settings and write changes to database."""

    def __init__(self, parent: ttk.Frame, controller: Controller):
        ttk.Frame.__init__(self, parent, style="Custom.TFrame")
        self.controller = controller
        label = tk.Label(self, text="Settings")
        label.pack(pady=10, padx=10)

        button = CustomButton(self, text="Back to Start Page", command=lambda: controller.show_frame(StartFrame))
        button.pack()
