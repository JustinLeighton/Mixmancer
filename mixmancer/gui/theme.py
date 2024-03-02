import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

class CustomTheme:
    def __init__(self, color):
        self.style = ttk.Style()
        self.color = color
        self.font_size = 12
        self.padding = (10, 5)
        self.borderwidth = 0

        self.style.theme_use('clam')
        self.style.configure("TFrame", background=self.color['grey'])

        self.style.configure('Custom.TButton',
                             background=self.color['grey'],
                             foreground=self.color['white'],
                             font=('Helvetica', self.font_size),
                             padding=self.padding,
                             relief='raised')

        self.style.configure('TLabel',
                             foreground=self.color['white'],
                             background=self.color['grey'],
                             font=('Helvetica', self.font_size))

        self.style.configure('Horizontal.TScale',
                             background=self.color['grey'],
                             troughcolor=self.color['purple'],
                             slidercolor=self.color['white'],
                             borderwidth=self.borderwidth)

class CustomButton(ttk.Button):
    def __init__(self, master=None, **kw):
        super().__init__(master, **kw)
        self.configure(style='Custom.TButton')

class CustomLabel(ttk.Label):
    def __init__(self, master=None, **kw):
        super().__init__(master, **kw)
        self.configure(style='Custom.TLabel')

class CustomSlider(ttk.Scale):
    def __init__(self, master=None, **kw):
        super().__init__(master, **kw)
        self.configure(style='Custom.Horizontal.TScale')

class CustomImage(ttk.Label):
    def __init__(self, master=None, image=None, **kw):
        super().__init__(master, **kw)
        self.image = image
        self.configure_image()

    def configure_image(self):
        if self.image:
            self.display_image()
        else:
            self.configure(text="N/A", font=("Helvetica", 12))

    def display_image(self):
        resized_image = self.image.resize((self.winfo_width(), self.winfo_height()), Image.ANTIALIAS)
        self.photo_image = ImageTk.PhotoImage(resized_image)
        self.configure(image=self.photo_image)

    def resize_image(self, event):
        if self.image:
            self.display_image()