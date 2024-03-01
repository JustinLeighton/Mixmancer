import tkinter as tk
from tkinter import ttk

class CustomButton(ttk.Button):
    def __init__(self, master=None, command=None, **kw):
        super().__init__(master, **kw)

        # Create a new style for the button
        style = ttk.Style()
        style.configure('CustomButton.TButton',
                        background='blue',        # Background color
                        foreground='white',       # Text color
                        font=('Helvetica', 12),   # Font and size
                        padding=(10, 5))          # Padding

        # Apply the custom style to the button
        self.configure(style='CustomButton.TButton')

        # Bind the button click event to the command function
        if command:
            self.configure(command=command)