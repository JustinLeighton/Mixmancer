import pytest
import tkinter as tk
from mixmancer.gui.popup import BasePopup


# Create the root window outside of any function or fixture
_root = tk.Tk()
_root.geometry("200x200")
_root.update_idletasks()


@pytest.fixture
def root():
    return _root


def test_init(root: tk.Tk):
    """Test initialization of BasePopup"""
    popup = BasePopup(root)
    assert popup.master == root


def test_on_mouse_wheel():
    """Test on_mouse_wheel method"""

    # Mock event object
    class MockEvent:
        def __init__(self, delta: int):
            self.delta = delta

    root = tk.Tk()
    popup = BasePopup(root)
    event = MockEvent(delta=120)
    popup.on_mouse_wheel(event)
    # Add assertions as needed


# Add more test cases for other methods as needed
