# -*- coding: utf-8 -*-
"""
Created on Thu May 18 23:31:42 2023

@author: Justin Leighton
"""

import pygame

from mixmancer.gui.frames import Controller, StartFrame, ImageFrame, MusicFrame, SfxFrame, SettingsFrame, MenuBar
from mixmancer.gui.theme import CustomTheme


class App(Controller):
    """Toplevel Tk widget"""

    def __init__(self):
        super().__init__()

        # Intitialize tkinter app
        self.title("Mixmancer")
        self.geometry(f"500x500")
        self.iconbitmap("assets/app/mixmancer.ico")  # type: ignore[reportUnknownMemberType]
        CustomTheme()

        # Initialize pygame
        pygame.init()
        pygame.mixer.init()

        # Initialize frames
        for F in (StartFrame, ImageFrame, MusicFrame, SfxFrame, SettingsFrame):
            frame = F(self.container, self)
            self.frames[F] = frame
        self.show_frame(StartFrame)

        # Initialize menu bar
        menubar = MenuBar(self)
        self.config(menu=menubar)


if __name__ == "__main__":
    app = App()
    app.mainloop()
