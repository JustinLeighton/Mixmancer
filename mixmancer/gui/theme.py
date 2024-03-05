import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from typing import Any, Optional, Callable


def calculate_resized_dimensions(image_dimensions: tuple[int, int], target_location: tuple[int, int]):
    """Calculate the resized dimensions of an image while maintaining aspect ratio,
    maximizing the space within the target location.

    Args:
    - image_dimensions (tuple): Dimensions of the original image (width, height).
    - target_location (tuple): Planned location of the image (x, y) within its container.

    Returns:
    - tuple: Resized dimensions (width, height).
    """
    # Unpack image dimensions
    image_width: int
    image_height: int
    available_width: int
    available_height: int
    image_width, image_height = image_dimensions
    available_width, available_height = target_location

    # Calculate aspect ratio of the original image
    try:
        aspect_ratio = image_width / image_height
    except ZeroDivisionError as e:
        raise ZeroDivisionError("Cannot calculate aspect ratio: Image height cannot be zero") from e

    # Calculate new dimensions while maintaining aspect ratio
    if available_width / aspect_ratio <= available_height:
        new_width = available_width
        new_height = int(new_width / aspect_ratio)
    else:
        new_height = available_height
        new_width = int(new_height * aspect_ratio)

    return new_width, new_height


class CustomTheme:
    """Custom theme for tkinter app and widgets

    Args:
        color (dict[str, str]): dictionary of color and hex value
        x (int, optional): horizontal pixal placement. Defaults to 0.
        y (int, optional): vertical pixal placement. Defaults to 0.
    """

    def __init__(self, color: dict[str, str], x: int = 0, y: int = 0):
        self.style: ttk.Style = ttk.Style()
        self.color: dict[str, str] = color
        self.font_size: int = 12
        self.padding: tuple[int, int] = (5, 5)
        self.borderwidth: int = 0
        self.x: int = x
        self.y: int = y

        self.style.theme_use("clam")

        frame_config: dict[str, Any] = {"background": self.color["grey"]}
        button_config: dict[str, Any] = {
            "background": self.color["grey"],
            "foreground": self.color["white"],
            "font": ("Helvetica", self.font_size),
            "padding": self.padding,
            "relief": "raised",
        }
        label_config: dict[str, Any] = {
            "foreground": self.color["white"],
            "background": self.color["grey"],
            "font": ("Helvetica", self.font_size),
        }
        scale_config: dict[str, Any] = {
            "background": self.color["grey"],
            "troughcolor": self.color["purple"],
            "slidercolor": self.color["white"],
            "borderwidth": self.borderwidth,
        }

        self.style.configure("TFrame", **frame_config)  # type: ignore[reportUnknownMemberType]
        self.style.configure("Custom.TButton", **button_config)  # type: ignore[reportUnknownMemberType]
        self.style.configure("TLabel", **label_config)  # type: ignore[reportUnknownMemberType]
        self.style.configure("Horizontal.TScale", **scale_config)  # type: ignore[reportUnknownMemberType]


class WidgetWithPlacement:
    """Widget parent class that allows for x and y pixel coordinates to be defined at class creation"""

    def __init__(self, master: tk.Tk, **kwargs: Any):
        self.x: int = kwargs.pop("x", 0)
        self.y: int = kwargs.pop("y", 0)
        super().__init__(master, **kwargs)  # type: ignore[reportCallIssue]

    def place(self, **kwargs: Any):
        """Places the widget at the specified x, y coordinates."""
        kwargs.update({"x": self.x, "y": self.y})
        super().place(**kwargs)  # type: ignore[unknownMemberType,E1101]


class CustomButton(WidgetWithPlacement, ttk.Button):
    """Custom ttk.Button widget with style theme"""

    def __init__(self, master: tk.Tk, **kwargs: Any):
        super().__init__(master, **kwargs)
        self.configure(style="Custom.TButton")


class CustomLabel(WidgetWithPlacement, ttk.Label):
    """Custom ttk.Label widget with style theme"""

    def __init__(self, master: tk.Tk, **kw: dict[str, Any]):
        super().__init__(master, **kw)
        self.configure(style="Custom.TLabel")


class CustomSlider(WidgetWithPlacement, ttk.Scale):
    """Custom ttk.Scale widget with style theme"""

    def __init__(self, master: tk.Tk, initial_value: float = 0.5, **kw: dict[str, Any]):
        super().__init__(master, **kw)
        self.configure(style="Custom.Horizontal.TScale")
        self.set(initial_value)  # type: ignore[unknownMemberType]


class CustomImage(WidgetWithPlacement, ttk.Label):
    """Custom ttk.Label widget to allow for the place method to be called at class creation and image auto resizing"""

    def __init__(self, master: tk.Tk, image_path: str = "", x: int = 0, y: int = 0, **kw: dict[str, Any]):
        super().__init__(master, **kw)
        self.image_path = image_path
        self.image_object: Image.Image
        self.image_photo: ImageTk.PhotoImage
        self.image_size: tuple[int, int] = (100, 100)
        self.image_dimension: tuple[int, int]
        self.x: int = x
        self.y: int = y
        self.configure_image()

    def configure_image(self, image_path: str = "", image_target_size: tuple[int, int] = (100, 100)):
        """Configure image if exists"""
        self.set_image_path(image_path)
        if self.image_path:
            self.load_image(self.image_path)
            self.resize_image(image_target_size)
        else:
            self.configure(text="N/A", font=("Helvetica", 12))

    def load_image(self, image_path: str):
        """Load PIL.Image.Image object from self.image_path"""
        if image_path:
            self.image_object = Image.open(image_path)
            self.image_dimension = self.image_object.size

    def display_image(self):
        """Display image on label widget, and auto resize to window"""
        resized_image: ImageTk.Image = self.image_object.resize(self.image_size, Image.Resampling.LANCZOS)  # type: ignore[unknownMemberType,E1101]
        self.image_photo = ImageTk.PhotoImage(resized_image)  # type: ignore[reportUnknownArgumentType]
        self.configure(image=self.image_photo)

    def resize_image(self, image_target_size: tuple[int, int]):
        """If an image is being displayed, call display_image to resize"""
        if self.image_path:
            self.image_size = calculate_resized_dimensions(self.image_dimension, image_target_size)
            self.display_image()

    def set_image_path(self, image_path: str):
        """Set image_path attribute

        Args:
            image_path (str): Path to image file
        """
        self.image_path = image_path


class SquareButton(tk.Button):
    """Custom tk.button widget for hexploration commands. Assigns callback function during object creation."""

    def __init__(
        self,
        master: tk.Tk,
        image: str = "",
        command: Optional[Callable[..., Any]] = None,
        color: Optional[dict[str, Any]] = None,
        **kwargs: Any
    ):
        super().__init__(master, **kwargs)  # type: ignore[reportArgumentType]
        self.image = image
        self.callback = command

        if self.image:
            self.photo_image = tk.PhotoImage(file=self.image)
            self.config(image=self.photo_image, compound="center")

        if self.callback:
            self.config(command=self.callback)

        if color:
            self.config(bg=color["grey"])
            self.config(fg="#ffffff")
            self.config(highlightbackground=color["white"])

        self.config(bd=1, relief="solid")
