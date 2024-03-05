import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from typing import Any, Callable, Optional


class CustomTheme:
    """
    Custom theme for tkinter app and widgets

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
    """
    Widget parent class that allows for x and y pixel coordinates to be defined at class creation
    """

    def __init__(self, master: tk.Tk, **kwargs: Any):
        self.x: int = kwargs.pop("x", 0)
        self.y: int = kwargs.pop("y", 0)
        super().__init__(master, **kwargs)  # type: ignore[reportCallIssue]

    def place(self, **kwargs: Any):
        """
        Places the widget at the specified x, y coordinates.
        """
        kwargs.update({"x": self.x, "y": self.y})
        super().place(**kwargs)  # type: ignore[unknownMemberType,E1101]


class CustomButton(WidgetWithPlacement, ttk.Button):
    """
    Custom ttk.Button widget to allow for the place method to be called at class creation
    """

    def __init__(self, master: tk.Tk, image_path: str = "", **kwargs: dict[str, Any]):
        super().__init__(master, **kwargs)
        if image_path:
            self.image = tk.PhotoImage(file=image_path)
            self.configure(image=self.image, compound="left")
        self.configure(style="Custom.TButton")


class CustomLabel(WidgetWithPlacement, ttk.Label):
    """
    Custom ttk.Label widget to allow for the place method to be called at class creation
    """

    def __init__(self, master: tk.Tk, **kw: dict[str, Any]):
        super().__init__(master, **kw)
        self.configure(style="Custom.TLabel")


class CustomSlider(WidgetWithPlacement, ttk.Scale):
    """
    Custom ttk.Scale widget to allow for the place method to be called at class creation
    """

    def __init__(self, master: tk.Tk, initial_value: float = 0.5, **kw: dict[str, Any]):
        super().__init__(master, **kw)
        self.configure(style="Custom.Horizontal.TScale")
        self.set(initial_value)  # type: ignore[unknownMemberType]


class CustomImage(WidgetWithPlacement, ttk.Label):
    """
    Custom ttk.Label widget to allow for the place method to be called at class creation and image auto resizing
    """

    def __init__(self, master: tk.Tk, image_path: str = "", x: int = 0, y: int = 0, **kw: dict[str, Any]):
        super().__init__(master, **kw)
        self.image = image_path
        self.x = x
        self.y = y
        self.configure_image()

    def configure_image(self):
        """Configure image if exists"""
        if self.image:
            self.display_image()
        else:
            self.configure(text="N/A", font=("Helvetica", 12))

    def display_image(self):
        """Display image on label widget, and auto resize to window"""
        resized_image: ImageTk.Image = self.image.resize((self.winfo_width(), self.winfo_height()), Image.ANTIALIAS)  # type: ignore[unknownMemberType,E1101]
        self.photo_image = ImageTk.PhotoImage(resized_image)  # type: ignore[reportUnknownArgumentType]
        self.configure(image=self.photo_image)

    def resize_image(self):
        """If an image is being displayed, call display_image to resize"""
        if self.image:
            self.display_image()


class SquareButton(tk.Button):
    """
    Custom tk.button widget for hexploration commands. Assigns callback function during object creation.
    """

    def __init__(
        self,
        master: tk.Tk,
        image: str = "",
        command: Optional[Callable[..., Any]] = None,
        color: Optional[dict[str, Any]] = None,
        **kwargs: dict[str, Any]
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
