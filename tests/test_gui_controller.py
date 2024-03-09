# import pytest
# import tkinter as tk
# from tkinter import ttk
# from PIL import Image, ImageTk
# import os

# from mixmancer.gui.frames import Controller


# _root = tk.Tk()
# _root.geometry("200x200")
# _root.update_idletasks()
# _controller = Controller()
# _frame = ttk.Frame()


# @pytest.fixture
# def root():
#     return _root


# @pytest.fixture
# def controller():
#     return _controller


# def test_initialization(controller: Controller):
#     assert isinstance(controller, Controller)
#     assert controller.container.winfo_exists()
#     assert isinstance(controller.frames, dict)
#     assert controller.image_projector is not None
#     assert controller.image_preview is None


# def test_show_frame(controller: Controller):
#     # Define a mock frame class
#     class MockFrame(ttk.Frame):
#         def __init__(self, parent, controller):  # type: ignore[reportUnknownMemberType]
#             super().__init__(parent)
#             self.controller = controller

#     mock_frame = MockFrame(controller.container, controller)
#     controller.frames[MockFrame] = mock_frame
#     controller.show_frame(MockFrame)
#     assert mock_frame.winfo_ismapped()


# def test_configure_theme(controller: Controller):
#     controller.configure_theme()
#     style = ttk.Style()
#     assert style.lookup("Custom.TFrame", "background") == "lightblue"  # type: ignore[reportUnknownMemberType]
#     assert style.lookup("Custom.TFrame", "foreground") == "black"  # type: ignore[reportUnknownMemberType]


# def test_display_image(controller: Controller):
#     test_image_path = "test_image.png"
#     test_img = Image.new("RGB", (100, 100), color="red")
#     test_img.save(test_image_path)
#     controller.display_image(test_image_path)
#     assert isinstance(controller.image_preview, ImageTk.PhotoImage)
#     os.remove(test_image_path)
