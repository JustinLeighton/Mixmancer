import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

class CustomTheme:
    def __init__(self, color, x=0, y=0):
        self.style = ttk.Style()
        self.color = color
        self.font_size = 12
        self.padding = (5, 5)
        self.borderwidth = 0
        self.x = x
        self.y = y

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

class WidgetWithPlacement:
    def __init__(self, master=None, **kwargs):
        self.x = kwargs.pop('x', 0)
        self.y = kwargs.pop('y', 0)
        super().__init__(master, **kwargs)

    def place(self, **kwargs):
        kwargs.update({'x': self.x, 'y': self.y})
        super().place(**kwargs)

class CustomButton(WidgetWithPlacement, ttk.Button):
    def __init__(self, master=None, image=None, **kw):
        super().__init__(master, **kw)
        if image:
            self.image = tk.PhotoImage(file=image)
            self.configure(image=self.image, compound='left')
        self.configure(style='Custom.TButton')

class CustomLabel(WidgetWithPlacement, ttk.Label):
    def __init__(self, master=None, **kw):
        super().__init__(master, **kw)
        self.configure(style='Custom.TLabel')

class CustomSlider(WidgetWithPlacement, ttk.Scale):
    def __init__(self, master=None, initial_value=None, **kw):
        super().__init__(master, **kw)
        self.configure(style='Custom.Horizontal.TScale')
        if initial_value is not None:
            self.set(initial_value)
        else:
            self.set(0.5)

class CustomImage(WidgetWithPlacement, ttk.Label):
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

class SquareButton(tk.Button):
    def __init__(self, master=None, image=None, command=None, color=None, **kwargs):
        super().__init__(master, **kwargs)
        self.image = image
        self.callback = command

        if self.image:
            self.photo_image = tk.PhotoImage(file=self.image)
            self.config(image=self.photo_image, compound='center')

        if self.callback:
            self.config(command=self.callback)

        if color:
            self.config(bg=color['grey'])
            self.config(fg='#ffffff')
            self.config(highlightbackground=color['white'])
        
        self.config(bd=1, relief="solid")