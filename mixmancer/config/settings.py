import json
from mixmancer.config.data_models import Coordinate


class Settings:
    """This class represents the settings of the application, such as resolution configurations, display preferences, and color schemes.
    Settings are initialized from a JSON file, allowing for easy modification and customization without altering the code.

    Attributes:
        projector_resolution (tuple[int, int]): The resolution settings for the projected image, expressed as width and height in pixels.
        app_resolution (tuple[int, int]): The resolution settings for the application window, expressed as width and height in pixels.
        display (int): The display preference for the application.
        color (dict): A dictionary containing color codes for various elements of the application UI, such as "white", "black", "grey", and "purple".

    Methods:
        __init__(filename='default_settings.json'): Initializes the Settings object by loading settings from the specified JSON file.
    """

    def __init__(self, path: str):
        self.color: dict[str, str] = {
            "white": "",
            "grey": "",
            "black": "",
            "purple": "",
        }
        self.app_resolution: tuple[int, int] = (500, 500)
        self.projector_resolution: tuple[int, int] = (1280, 900)
        self.display: int = 1
        self.hexmap_offset: tuple[int, int] = (0, 0)
        self.hexmap_start: tuple[int, int] = (10, 5)
        self.hex_size = 56
        try:
            self.from_json(path)
        except FileNotFoundError:
            raise FileNotFoundError(f"Settings file 'mixmancer/config/settings.json' not found.")

    def set_projector_resolution(self, resolution: Coordinate):
        self.projector_resolution = resolution()

    def get_projector_resolution(self) -> Coordinate:
        return Coordinate(*self.projector_resolution)

    def set_app_resolution(self, height: int, width: int):
        self.app_resolution = height, width

    def get_app_resolution(self) -> Coordinate:
        return Coordinate(*self.app_resolution)

    def set_hexmap_offset(self, offset: Coordinate):
        self.hexmap_offset = offset()

    def get_hexmap_offset(self) -> Coordinate:
        return Coordinate(*self.hexmap_offset)

    def set_hexmap_start(self, start: Coordinate):
        self.hexmap_start = start()

    def get_hexmap_start(self) -> Coordinate:
        return Coordinate(*self.hexmap_start)

    def to_json(self, filename: str):
        """Export settings to json"""
        with open(filename, "w") as f:
            json.dump(self.__dict__, f)

    def from_json(self, filename: str):
        """Import settings to json"""
        with open(filename, "r") as f:
            data = json.load(f)
        self.check_keys(data)
        self.__dict__.update(data)

    def check_keys(self, data: dict[str, str]):
        """Check to ensure all keys import correctly from json file"""
        expected_keys = [attr for attr in dir(self) if not attr.startswith("__") and not callable(getattr(self, attr))]
        missing_keys = [key for key in expected_keys if key not in data]
        if missing_keys:
            raise ValueError(f"Missing keys in settings JSON: {', '.join(missing_keys)}")
        if "color" in data:
            for color_key in data["color"]:
                if color_key not in self.color:
                    raise ValueError(f"Missing color key '{color_key}' in settings JSON.")
