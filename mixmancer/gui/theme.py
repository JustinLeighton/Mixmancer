from tkinter import ttk
from PIL import Image, ImageTk
from typing import Any, Optional, Callable
from mixmancer.config.settings import Settings


class CustomTheme:
    """Custom theme for tkinter app and widgets

    Args:
        color (dict[str, str]): dictionary of color and hex value
        x (int, optional): horizontal pixal placement. Defaults to 0.
        y (int, optional): vertical pixal placement. Defaults to 0.
    """

    def __init__(self, settings: Settings):
        self.style = ttk.Style()
        self.color = settings.color
        self.font_size: int = 12
        self.padding: tuple[int, int] = (5, 5)
        self.borderwidth: int = 0

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
        entry_config: dict[str, Any] = {
            "background": self.color["grey"],
            "foreground": self.color["white"],
            "font": ("Helvetica", self.font_size),
            "padding": self.padding,
            "borderwidth": self.borderwidth,
        }
        square_button_config: dict[str, Any] = {
            "background": self.color["grey"],
            "foreground": self.color["white"],
            "font": ("Helvetica", self.font_size),
            "padding": self.padding,
            "relief": "raised",
            "width": 1,
            "height": 1,
        }

        self.style.configure("TFrame", **frame_config)  # type: ignore[reportUnknownMemberType]
        self.style.configure("Custom.TFrame", **frame_config)  # type: ignore[reportUnknownMemberType]
        self.style.configure("Custom.TButton", **button_config)  # type: ignore[reportUnknownMemberType]
        self.style.configure("TLabel", **label_config)  # type: ignore[reportUnknownMemberType]
        self.style.configure("Horizontal.TScale", **scale_config)  # type: ignore[reportUnknownMemberType]
        self.style.configure("Custom.TEntry", **entry_config)  # type: ignore[reportUnknownMemberType]
        self.style.configure("Square.TButton", **square_button_config)  # type: ignore[reportUnknownMemberType]


class CustomButton(ttk.Button):
    """Custom ttk.Button widget with style theme"""

    def __init__(self, master: ttk.Frame, **kwargs: Any):
        super().__init__(master, **kwargs)
        self.configure(style="Custom.TButton")
        # self.configure(bg="#000000", fg="#b7f731", relief="flat", width=20)


class CustomLabel(ttk.Label):
    """Custom ttk.Label widget with style theme"""

    def __init__(self, master: ttk.Frame, **kw: Any):
        super().__init__(master, **kw)
        self.configure(style="Custom.TLabel")


class CustomSlider(ttk.Scale):
    """Custom ttk.Scale widget with style theme"""

    def __init__(self, master: ttk.Frame, initial_value: float = 0.5, **kw: Any):
        super().__init__(master, **kw)
        self.configure(style="Custom.Horizontal.TScale")
        self.set(initial_value)  # type: ignore[unknownMemberType]


class CustomImage(ttk.Label):
    """Custom ttk.Label widget to allow for the place method to be called at class creation and image auto resizing"""

    def __init__(self, master: ttk.Frame, **kw: Any):
        super().__init__(master, **kw)
        self.image_pil: Optional[Image.Image]
        self.image_photo: ImageTk.PhotoImage
        self.image_size: tuple[int, int] = (100, 100)
        self.image_dimension: tuple[int, int]


class CustomEntry(ttk.Entry):
    """Custom ttk.Entry widget with style theme"""

    def __init__(self, master: ttk.Frame, **kwargs: Any):
        super().__init__(master, **kwargs)
        self.configure(style="Custom.TEntry")


class SquareButton(ttk.Button):
    """Custom tk.button widget for hexploration commands. Assigns callback function during object creation.

    Args:
        master (ttk.Frame): Master frame
        coordinates (tuple[int, int]): Coordinates x/y for placement within subframe
        image_path (str, optional): Path to image file. Defaults to "".
        command (Optional[Callable[..., Any]], optional): Callback function. Defaults to None.
    """

    def __init__(
        self,
        master: ttk.Frame,
        coordinates: tuple[int, int],
        image_path: str = "",
        command: Optional[Callable[..., Any]] = None,
        **kwargs: Any
    ):
        super().__init__(master, **kwargs)  # type: ignore[reportArgumentType]
        self.image_path = image_path
        self.command = command
        self.coordinates = coordinates
        self.configure(style="Square.TButton")

        if self.image_path:

            # Load the image
            img = Image.open(image_path)
            img.thumbnail((20, 20))
            self.photo_image = ImageTk.PhotoImage(img)
            self.config(image=self.photo_image, compound="center")
            self.image = self.photo_image

        if self.command:
            self.config(command=self.command)
