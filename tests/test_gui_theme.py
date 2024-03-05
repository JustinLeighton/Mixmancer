import pytest
import tkinter as tk
from tkinter import ttk
from mixmancer.gui.theme import (
    calculate_resized_dimensions,
    CustomTheme,
    CustomButton,
    CustomLabel,
    CustomSlider,
    CustomImage,
    SquareButton,
)
from typing import Any


@pytest.fixture
def custom_theme():
    color = {"grey": "#CCCCCC", "white": "#FFFFFF", "purple": "#800080"}
    return CustomTheme(color)


# Create the root window outside of any function or fixture
_root = tk.Tk()
_root.geometry("200x200")
_root.update_idletasks()


@pytest.fixture
def root():
    return _root


@pytest.fixture(scope="session", autouse=True)
def close_root():
    yield
    _root.destroy()


# Define test cases
@pytest.mark.parametrize(
    "image_dimension, target_location_list, expected_dimensions_list",
    [
        (
            (800, 600),
            [(200, 150), (400, 300), (1066, 800), (50, 50), (2000, 50)],
            [(200, 150), (400, 300), (1066, 799), (50, 37), (66, 50)],
        ),
    ],
)
def test_calculate_resized_dimensions(
    image_dimension: tuple[int, int],
    target_location_list: tuple[tuple[int, int]],
    expected_dimensions_list: tuple[tuple[int, int]],
):

    # Check if the output matches the expected result for each target location
    for target_location, expected_dimension in zip(target_location_list, expected_dimensions_list):
        resized_dimension = calculate_resized_dimensions(image_dimension, target_location)
        assert resized_dimension == expected_dimension

    # Check for zero division error
    with pytest.raises(ZeroDivisionError):
        calculate_resized_dimensions((0, 0), (100, 100))


def test_custom_theme_initialization(custom_theme: CustomTheme):
    assert isinstance(custom_theme.style, ttk.Style)
    assert custom_theme.font_size == 12
    assert custom_theme.padding == (5, 5)
    assert custom_theme.borderwidth == 0
    assert custom_theme.x == 0
    assert custom_theme.y == 0


def test_style_configuration(custom_theme: CustomTheme):
    frame_config = custom_theme.style.lookup("TFrame", "background")  # type: ignore[reportUnknownMemberType]
    assert frame_config == custom_theme.color["grey"]

    button_config = custom_theme.style.lookup("Custom.TButton", "background")  # type: ignore[reportUnknownMemberType]
    assert button_config == custom_theme.color["grey"]
    assert custom_theme.style.lookup("Custom.TButton", "foreground") == custom_theme.color["white"]  # type: ignore[reportUnknownMemberType]
    assert custom_theme.style.lookup("Custom.TButton", "font") == "Helvetica 12"  # type: ignore[reportUnknownMemberType]
    assert custom_theme.style.lookup("Custom.TButton", "padding") == "5 5"  # type: ignore[reportUnknownMemberType]
    assert custom_theme.style.lookup("Custom.TButton", "relief") == "raised"  # type: ignore[reportUnknownMemberType]

    label_config = custom_theme.style.lookup("TLabel", "foreground")  # type: ignore[reportUnknownMemberType]
    assert label_config == custom_theme.color["white"]
    assert custom_theme.style.lookup("TLabel", "background") == custom_theme.color["grey"]  # type: ignore[reportUnknownMemberType]
    assert custom_theme.style.lookup("TLabel", "font") == "Helvetica 12"  # type: ignore[reportUnknownMemberType]

    scale_config = custom_theme.style.lookup("Horizontal.TScale", "background")  # type: ignore[reportUnknownMemberType]
    assert scale_config == custom_theme.color["grey"]
    assert custom_theme.style.lookup("Horizontal.TScale", "troughcolor") == custom_theme.color["purple"]  # type: ignore[reportUnknownMemberType]
    assert custom_theme.style.lookup("Horizontal.TScale", "slidercolor") == custom_theme.color["white"]  # type: ignore[reportUnknownMemberType]
    assert custom_theme.style.lookup("Horizontal.TScale", "borderwidth") == custom_theme.borderwidth  # type: ignore[reportUnknownMemberType]


def test_custom_button_creation(root: tk.Tk):
    button = CustomButton(root, text="Test Button")
    assert isinstance(button, CustomButton)
    assert isinstance(button, ttk.Button)
    assert button.master == root
    assert button.cget("text") == "Test Button"


def test_custom_button_placement(root: tk.Tk):
    config = {
        "text": "Test Button",
        "command": lambda: print("Hello World!"),
        "x": 10,
        "y": 290,
    }
    widget_class = CustomButton
    kwargs = {key: value for key, value in config.items()}
    widget = widget_class(root, **kwargs)
    widget.place(x=config["x"], y=config["y"])
    root.update()
    assert widget.winfo_x() == 10
    assert widget.winfo_y() == 290
    assert widget.cget("text") == "Test Button"


def test_custom_label_creation(root: tk.Tk):
    label = CustomLabel(root)
    assert isinstance(label, CustomLabel)
    assert isinstance(label, ttk.Label)
    assert label.master == root


def test_custom_label_placement(root: tk.Tk):
    config = {"text": "Test Label", "x": 10, "y": 90}
    widget_class = CustomLabel
    kwargs: dict[str, Any] = {key: value for key, value in config.items()}
    widget = widget_class(root, **kwargs)
    widget.place(x=config["x"], y=config["y"])
    root.update()
    assert widget.winfo_x() == 10
    assert widget.winfo_y() == 90
    assert widget.cget("text") == "Test Label"


def test_custom_slider_creation(root: tk.Tk):
    slider = CustomSlider(root)
    assert isinstance(slider, CustomSlider)
    assert isinstance(slider, ttk.Scale)
    assert slider.master == root


def test_custom_slider_placement(root: tk.Tk):
    config = {"x": 10, "y": 90}
    widget_class = CustomLabel
    kwargs: dict[str, Any] = {key: value for key, value in config.items()}
    widget = widget_class(root, **kwargs)
    widget.place(x=config["x"], y=config["y"])
    root.update()
    assert widget.winfo_x() == 10
    assert widget.winfo_y() == 90


def test_custom_image_creation(root: tk.Tk):
    label = CustomImage(root)
    assert isinstance(label, CustomImage)
    assert isinstance(label, ttk.Label)
    assert label.master == root


def test_custom_image_placement(root: tk.Tk):
    config = {"x": 150, "y": 10}
    widget_class = CustomImage
    kwargs: dict[str, Any] = {key: value for key, value in config.items()}
    widget = widget_class(root, **kwargs)
    widget.place(x=config["x"], y=config["y"])
    root.update()
    assert widget.winfo_x() == 150
    assert widget.winfo_y() == 10
    assert widget.cget("text") == "N/A"


def test_custom_image_display(root: tk.Tk):
    config = {"x": 150, "y": 10}
    widget_class = CustomImage
    kwargs: dict[str, Any] = {key: value for key, value in config.items()}
    widget = widget_class(root, **kwargs)
    widget.place(x=config["x"], y=config["y"])
    image_path = "assets/tests/test_wide.jpg"
    assert widget.cget("text") == "N/A"
    if image_path:
        widget.configure_image(image_path)
        assert widget.image_object is not None
        assert widget.image_path == image_path
        assert widget.image_object is not None
    else:
        pytest.fail(f"Image file not found: {image_path}")


def test_custom_square_button_creation(root: tk.Tk):
    button = SquareButton(
        root,
        image=f"assets/tests/button.png",
        color={
            "white": "#ffffff",
            "black": "#000000",
            "grey": "#36393f",
            "purple": "#7289da",
        },
        command=lambda: 2,
    )
    button.place(x=40, y=330)
    root.update()
    assert button.winfo_x() == 40
    assert button.winfo_y() == 330
