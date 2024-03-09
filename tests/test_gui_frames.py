# import pytest
# import tkinter as tk
# from tkinter import ttk
# from unittest.mock import Mock
# import os
# from PIL import Image
# from mixmancer.gui.frames import Controller, StartFrame, ImageFrame, MusicFrame, SfxFrame, SettingsFrame


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


# @pytest.fixture
# def parent():
#     return _frame


# @pytest.fixture
# def start_frame(root: ttk.Frame = _frame) -> StartFrame:
#     controller_mock = Mock()
#     return StartFrame(parent=_frame, controller=controller_mock)


# @pytest.fixture
# def image_frame(root: ttk.Frame = _frame):
#     controller_mock = Mock()
#     image_frame = ImageFrame(parent=_frame, controller=controller_mock)
#     return image_frame


# @pytest.fixture
# def music_frame(root: ttk.Frame = _frame):
#     controller_mock = Mock()
#     music_frame = MusicFrame(parent=_frame, controller=controller_mock)
#     return music_frame


# @pytest.fixture
# def sfx_frame(root: ttk.Frame = _frame):
#     controller_mock = Mock()
#     sfx_frame = SfxFrame(parent=_frame, controller=controller_mock)
#     return sfx_frame


# @pytest.fixture
# def settings_frame(root: ttk.Frame = _frame):
#     controller_mock = Mock()
#     settings_frame = SettingsFrame(parent=_frame, controller=controller_mock)
#     return settings_frame


# @pytest.fixture
# def mock_controller():
#     class MockController:
#         def display_image(self, image_path: str):
#             pass

#         def show_frame(self, frame_class: tk.Frame):
#             pass

#     return MockController()


# def test_initialization(image_frame: ImageFrame):
#     assert isinstance(image_frame, ImageFrame)
#     assert isinstance(image_frame.canvas, tk.Canvas)
#     assert isinstance(image_frame.scrollbar, ttk.Scrollbar)
#     assert isinstance(image_frame.inner_frame, ttk.Frame)
#     assert image_frame.thumbnail_buttons == []


# def test_display_image_thumbnails(image_frame: ImageFrame):
#     # Create a temporary directory with image files for testing
#     test_dir = "test_images"
#     os.makedirs(test_dir, exist_ok=True)
#     test_image_paths = []

#     try:
#         # Create some test image files
#         for i in range(5):
#             img = Image.new("RGB", (100, 100), color=(i * 50, i * 50, i * 50))
#             img_path = os.path.join(test_dir, f"test_image_{i}.jpg")
#             img.save(img_path)
#             test_image_paths.append(img_path)

#         # Call display_image_thumbnails
#         image_frame.display_image_thumbnails(test_dir)

#         # Check if thumbnail buttons are created
#         assert len(image_frame.thumbnail_buttons) == 5
#         for btn in image_frame.thumbnail_buttons:
#             assert isinstance(btn, tk.Button)

#     finally:
#         # Cleanup
#         for img_path in test_image_paths:
#             os.remove(img_path)
#         os.rmdir(test_dir)


# def test_thumbnail_selected(image_frame: ImageFrame, mock_controller: Controller):
#     # Define a mock image path
#     image_path = "test_image.jpg"

#     # Call thumbnail_selected method
#     image_frame.controller = mock_controller
#     image_frame.thumbnail_selected(image_path)

#     # Assert that display_image and show_frame methods are called in the controller
#     assert image_frame.controller.display_image.called_with(image_path)
#     assert image_frame.controller.show_frame.called_with(StartFrame)


# def test_music_frame_initialization(music_frame: MusicFrame):
#     assert isinstance(music_frame, ttk.Frame)
#     assert music_frame.winfo_class() == "TFrame"
#     assert len(music_frame.winfo_children()) == 2


# def test_music_button_command(music_frame: MusicFrame):
#     show_frame_mock = Mock()
#     music_frame.controller.show_frame = show_frame_mock
#     music_frame.winfo_children()[-1].invoke()  # type: ignore
#     assert show_frame_mock.called_with(StartFrame)


# def test_sfx_frame_initialization(sfx_frame: SfxFrame):
#     assert isinstance(sfx_frame, ttk.Frame)
#     assert sfx_frame.winfo_class() == "TFrame"
#     assert len(sfx_frame.winfo_children()) == 2


# def test_sfx_button_command(sfx_frame: SfxFrame):
#     show_frame_mock = Mock()
#     sfx_frame.controller.show_frame = show_frame_mock
#     sfx_frame.winfo_children()[-1].invoke()  # type: ignore
#     assert show_frame_mock.called_with(StartFrame)


# def test_settings_frame_initialization(settings_frame: SettingsFrame):
#     assert isinstance(settings_frame, ttk.Frame)
#     assert settings_frame.winfo_class() == "TFrame"
#     assert len(settings_frame.winfo_children()) == 2


# def test_settings_button_command(settings_frame: SettingsFrame):
#     show_frame_mock = Mock()
#     settings_frame.controller.show_frame = show_frame_mock
#     settings_frame.winfo_children()[-1].invoke()  # type: ignore
#     assert show_frame_mock.called_with(StartFrame)
