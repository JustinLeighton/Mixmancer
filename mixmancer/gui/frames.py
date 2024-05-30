import tkinter as tk
from tkinter import ttk
import os
from PIL import Image, ImageTk

from typing import Literal, Union, Any, Callable

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

        # Sfx stopper
        self.button_container["sfx_stopper"] = CustomButton(
            self.left_frame, text="Stop Effect", command=controller.mixer.stop_sfx_sounds
        )

        # Hexmap button
        self.button_container["hexmap_selector"] = CustomButton(
            self.left_frame, text="Hexmap", command=controller.display_hexmap
        )

        # Hexmap frame
        self.button_container["hexmap_frame"] = HexMapFrame(self.left_frame, self.controller)

        # Place widgets
        for _, widget in self.button_container.items():
            widget.pack(padx=5, pady=5)

        # Image preview
        self.label_image_preview = CustomImage(self.right_frame)
        self.label_image_preview.pack(anchor=tk.NW, pady=5)
        self.bind("<Configure>", self.resize_preview_image)  # type: ignore

    def update(self):
        """Modify update method to update the configured preview image"""
        super().update()
        self.update_preview_image()
        self.button_container["hexmap_frame"].update()
        self.update_labels()

    def update_preview_image(self):
        """Update preview image in app window"""
        if self.controller.image_preview is not None:  # type: ignore[reportUnnecessaryComparison]
            self.controller.update_thumnail_image()
            self.label_image_preview.configure(image=self.controller.image_preview)

    def update_labels(self):
        """Update label text in app window"""
        self.button_container["image_selection"].configure(text=self.controller.image_projector.get_current_image())  # type: ignore
        self.button_container["music_selection"].configure(text=self.controller.mixer.get_current_track())  # type: ignore

    def resize_preview_image(self, event: Literal[tk.EventType.ResizeRequest]):
        """Resizes preview image on app window when window resizes

        Args:
            event (Literal[tk.EventType.ResizeRequest]): Tkinter window resize event
        """
        if event.widget == self:  # type: ignore[reportUnknownMemberType]
            if (event.width, event.height) != self.controller.settings.app_resolution:  # type: ignore[reportUnknownMemberType]
                self.controller.settings.set_app_resolution(event.width, event.height)  # type: ignore[reportUnknownMemberType]
                self.controller.image_thumbnail_dimensions = self.get_preview_image_size()
                self.update_preview_image()

    def get_preview_image_size(self, padding: int = 5) -> tuple[int, int]:
        """Get size available for preview image within app window"""
        image_width: int = int(self.controller.settings.get_app_resolution().x - 150 - padding * 2)
        image_height: int = int(self.controller.settings.get_app_resolution().y - 5 - padding * 2)
        if image_width < 100 or image_height < 100:
            image_width, image_height = 100, 100
        return image_width, image_height


class ImageFrame(ttk.Frame):
    """Display .jpg/.jpeg/.png files in assets/img for selection"""

    def __init__(self, parent: ttk.Frame, controller: Controller):
        ttk.Frame.__init__(self, parent, style="Custom.TFrame")
        self.controller = controller

        # Create a search bar
        self.query: str = ""
        self.search_var = tk.StringVar()
        self.search_var.trace_add("write", self.filter_images)
        self.search_entry = ttk.Entry(self, textvariable=self.search_var)
        self.search_entry.pack(side="top", fill="x")

        # Create a canvas for scrollable content
        background: str = ttk.Style().lookup("TFrame", "background")  # type: ignore
        self.canvas = tk.Canvas(self, highlightthickness=0, background=background)  # type: ignore
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
            btn.configure(text=image_file)
            self.thumbnail_buttons.append(btn)
        self.layout_thumbnails()

    def layout_thumbnails(self):
        """Dynamically adjusts thumbnail layout based on window width"""
        for widget in self.inner_frame.winfo_children():
            widget.grid_forget()
        width = self.winfo_width()
        num_columns = max(1, width // 120)
        counter = 0
        for _, btn in enumerate(self.thumbnail_buttons):
            if self.query in btn["text"].lower():
                row = counter // num_columns
                column = counter % num_columns
                btn.grid(row=row, column=column, padx=5, pady=5)
                counter += 1

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

    def filter_images(self, *args: Any):
        """Filter the list of sound effects based on the search query"""
        self.query = self.search_var.get().lower()
        self.layout_thumbnails()


class SearchableFrame(ttk.Frame):
    """Main selection frame for music and sound effects, with searchability"""

    def __init__(
        self,
        parent: ttk.Frame,
        controller: Controller,
        file_directory: str,
        extension: str,
        callback: Callable[..., Any],
    ):
        ttk.Frame.__init__(self, parent, style="Custom.TFrame")
        self.controller = controller
        self.file_dir = file_directory
        self.extension = extension
        self.callback = callback
        self.buttons: list[ttk.Button] = []

        self.search_var = tk.StringVar()
        self.search_var.trace_add("write", self.filter_sfx_list)
        search_entry = ttk.Entry(self, textvariable=self.search_var, width=20)
        search_entry.pack(side=tk.TOP, padx=10, pady=10)

        self.load_buttons()

    def load_buttons(self):
        """Load sound effect buttons"""
        if os.path.isdir(self.file_dir):
            self.buttons.clear()
            mp3_files = [file for file in os.listdir(self.file_dir) if file.lower().endswith(self.extension)]
            for mp3_file in mp3_files:
                selectable_file = os.path.join(self.file_dir, mp3_file)
                button = ttk.Button(self, text=mp3_file, command=lambda file=selectable_file: self.sfx_selected(file))
                button.pack()
                self.buttons.append(button)

    def sfx_selected(self, selectable_file: str):
        """Function to execute when a sfx file button is selected"""
        self.callback(selectable_file)
        self.controller.show_frame(StartFrame)

    def filter_sfx_list(self, *args: Any):
        """Filter the list of sound effects based on the search query"""
        query = self.search_var.get().lower()
        for button in self.buttons:
            if query in button["text"].lower():
                button.pack()
            else:
                button.pack_forget()


class MusicFrame(SearchableFrame):
    """Display .mp3 files in assets/music for selection"""

    def __init__(self, parent: ttk.Frame, controller: Controller):
        SearchableFrame.__init__(
            self,
            parent,
            controller,
            file_directory="assets/music",
            extension=".mp3",
            callback=controller.mixer.play_music,
        )


class SfxFrame(SearchableFrame):
    """Display wav in assets/sfx files for selection"""

    def __init__(self, parent: ttk.Frame, controller: Controller):
        SearchableFrame.__init__(
            self,
            parent,
            controller,
            file_directory="assets/sfx",
            extension=".wav",
            callback=controller.mixer.play_sfx,
        )


class HexMapFrame(ttk.Frame):
    """Container for hexmap control buttons"""

    def __init__(self, parent: ttk.Frame, controller: Controller, width: int = 120, height: int = 300):
        ttk.Frame.__init__(self, parent, style="Custom.TFrame")
        self.controller = controller
        self.parent = parent
        self.config(width=width, height=height)
        self.visible = False
        self.button_container: dict[str, SquareButton] = {}
        self.button_config: dict[str, tuple[int, int]] = {
            "upper_left": (20, 0),
            "upper_right": (60, 0),
            "left": (0, 40),
            "right": (80, 40),
            "lower_left": (20, 80),
            "lower_right": (60, 80),
            "history": (0, 120),
            "undo": (40, 120),
            "fog": (80, 120),
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
        ttk.Frame().update()
        if self.visible and not self.controller.hexmap_flag:
            self.hide_buttons()
        elif not self.visible and self.controller.hexmap_flag:
            self.show_buttons()

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
            btn.place(x=x, y=y)


class SettingsFrame(ttk.Frame):
    """Settings menu. Change settings and write changes to database."""

    def __init__(self, parent: ttk.Frame, controller: Controller):
        ttk.Frame.__init__(self, parent, style="Custom.TFrame")
        self.controller = controller
        self.settings = self.controller.settings

        # Header
        ttk.Label(self, text="Settings").pack()

        # Projector
        ttk.Label(self, text="\nProjector").pack(anchor="w")
        self.resolution = CoordinateEntry(self, "Resolution", self.settings.projector_resolution)
        self.display = CoordinateEntry(self, "Display", tuple([self.settings.display]))

        # Hexmap
        ttk.Label(self, text="\nHexmap").pack(anchor="w")
        self.hexmap_size = CoordinateEntry(self, "Hex Size", tuple([self.settings.hex_size]))
        self.hexmap_offset = CoordinateEntry(self, "Offset", self.settings.hexmap_offset)
        self.hexmap_start = CoordinateEntry(self, "Start", self.settings.hexmap_start)

        # Buttons
        button_frame = ttk.Frame(self, style="Custom.TFrame")
        CustomButton(button_frame, text="Accept", command=lambda: self.update_settings()).pack(side=tk.LEFT)
        CustomButton(button_frame, text="Cancel", command=lambda: controller.show_frame(StartFrame)).pack(side=tk.LEFT)
        button_frame.pack(pady=10)

    def update_settings(self):
        self.settings.projector_resolution = self.resolution.get()  # type: ignore
        self.settings.display = self.display.get()[0]
        self.settings.hex_size = self.hexmap_size.get()[0]
        self.settings.hexmap_offset = self.hexmap_offset.get()  # type: ignore
        self.settings.hexmap_start = self.hexmap_start.get()  # type: ignore
        self.controller.update_settings(self.settings)
        self.controller.show_frame(StartFrame)


class CoordinateEntry(ttk.Frame):
    def __init__(self, master: ttk.Frame, label: str, values: tuple[int, ...]):
        ttk.Frame.__init__(self, master=master, style="Custom.TFrame")
        label_frame = ttk.Frame(self, width=100, height=20, style="Custom.TFrame")
        label_frame.pack_propagate(False)
        ttk.Label(label_frame, text=label).pack(side=tk.LEFT)
        label_frame.pack(side=tk.LEFT, padx=2, pady=2)
        self.entry_boxes: list[ttk.Entry] = []
        for v in values:
            self.entry_boxes.append(self.generate_entry(v))
        self.pack(anchor="w")

    def generate_entry(self, value: int) -> ttk.Entry:
        widget = ttk.Entry(self, validate="key", validatecommand=(self.register(self.validate_int), "%P"), width=5)
        widget.pack(side=tk.LEFT, padx=2, pady=2)
        widget.insert(0, str(value))
        return widget

    def validate_int(self, value_if_allowed: str) -> bool:
        return value_if_allowed.isdigit() or value_if_allowed == ""

    def get(self) -> tuple[int, ...]:
        return tuple(int(x.get()) for x in self.entry_boxes)


class MenuFrame(ttk.Frame):
    """Settings menu. Change settings and write changes to database."""

    def __init__(self, parent: ttk.Frame, controller: Controller):
        ttk.Frame.__init__(self, parent, style="Custom.TFrame")


class MenuBar(tk.Menu):
    """Top menu bar of application window"""

    def __init__(self, controller: Controller):
        super().__init__()

        # Create a "File" menu
        file_menu = tk.Menu(self, tearoff=0)
        file_menu.add_command(label="Home", command=lambda: controller.show_frame(StartFrame))
        file_menu.add_command(label="Settings", command=lambda: controller.show_frame(SettingsFrame))
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=controller.destroy)
        self.add_cascade(label="File", menu=file_menu)


def get_frames():
    return StartFrame, ImageFrame, MusicFrame, SfxFrame, SettingsFrame
