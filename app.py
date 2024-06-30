# -*- coding: utf-8 -*-
"""
Created on Thu May 18 23:31:42 2023

@author: Justin Leighton
"""

import threading
import argparse

import pygame

from mixmancer.gui.frames import Controller, StartFrame, MenuBar, get_frames
from mixmancer.api.api import start_fastapi, data_queue
from mixmancer.config.parameters import FRAME_RATE


class App(Controller):
    """Toplevel Tk widget"""

    def __init__(self):
        super().__init__()

        # Intitialize tkinter app
        self.title("Mixmancer")
        self.geometry(f"500x500")
        self.iconbitmap("assets/app/mixmancer.ico")  # type: ignore[reportUnknownMemberType]

        # Initialize pygame
        pygame.init()
        pygame.mixer.init()
        self.clock = pygame.time.Clock()

        # Initialize frames
        for F in get_frames():
            frame = F(self.container, self)
            self.frames[F] = frame
        self.show_frame(StartFrame)

        # Initialize menu bar
        menubar = MenuBar(self)
        self.config(menu=menubar)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the app with or without API thread.")
    parser.add_argument("-local", action="store_true", help="Run the app without API thread")
    args = parser.parse_args()

    if not args.local:
        thread = threading.Thread(target=start_fastapi)
        thread.daemon = True
        thread.start()

    app = App()
    while True:
        app.update()
        app.clock.tick(FRAME_RATE)

        # Check the queue for new data
        while not data_queue.empty():
            data = data_queue.get()
            app.process_data(data)
