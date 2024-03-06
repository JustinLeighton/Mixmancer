import pytest
import tkinter as tk
from tkinter import ttk
from mixmancer.gui.popup import BasePopup, ImagePopup
from unittest.mock import Mock


# Create the root window outside of any function or fixture
_root = tk.Tk()
_root.attributes("-topmost", False)  # type: ignore
_root.geometry("200x200")
_root.update_idletasks()


@pytest.fixture
def root():
    return _root


@pytest.fixture(scope="session", autouse=True)
def close_root():
    yield
    _root.destroy()


def test_init(root: tk.Tk):
    """Test initialization of BasePopup"""
    popup = BasePopup(root)
    assert isinstance(popup, tk.Toplevel)
    assert popup.master == root


def test_open_popup(root: tk.Tk):
    """Test the _open_popup method"""
    popup = BasePopup(root)
    popup._open_popup()  # type: ignore[reportPrivateUsage]
    # No assertions, just ensure the method doesn't raise an exception


def test_get_mouse_position(root: tk.Tk):
    """Test the _get_mouse_position method"""
    popup = BasePopup(root)
    x, y = popup._get_mouse_position()  # type: ignore[reportPrivateUsage]
    assert isinstance(x, int)
    assert isinstance(y, int)


def test_make_scrollable(root: tk.Tk):
    """Test the make_scrollable method"""
    popup = BasePopup(root)
    scrollable_frame: ttk.Frame = popup.make_scrollable()
    assert isinstance(scrollable_frame, ttk.Frame)

    # Verify that the canvas and scrollbar are present
    assert isinstance(popup.children["!canvas"], tk.Canvas)
    assert isinstance(popup.children["!scrollbar"], ttk.Scrollbar)


def test_image_popup_initialization(root: tk.Tk):
    """Test initialization of ImagePopup"""

    def callback(selected_image: str):
        pass  # Dummy callback function

    image_popup = ImagePopup(root, "assets/tests", callback)
    assert image_popup.winfo_exists()  # Check if the window is created

    # Check if the title is set correctly
    assert image_popup.title() == "Select Image"

    # Check if the geometry is set correctly
    assert image_popup.winfo_width() == 500
    assert image_popup.winfo_height() == 300


def test_image_popup_buttons(root: tk.Tk):
    def callback(selected_image: str):
        pass  # Dummy callback function

    image_popup = ImagePopup(root, "assets/tests", callback)

    # Check if buttons are created for each image
    buttons = image_popup.children.values()
    assert any("test_tall.jpg" == item[0] for item in image_popup.images)
    assert len(buttons) == len(image_popup.images)


def test_select_image(root: tk.Tk):
    mock_callback = Mock()
    image_popup = ImagePopup(root, "assets/tests", mock_callback)
    index = 0
    image_popup.select_image(index)
    assert image_popup.callback.called_with(image_popup.images[index][0])  # type: ignore
    assert not image_popup.winfo_exists()
