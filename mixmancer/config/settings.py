class Settings:
    """
    Object to hold app settings. Plan to move this into json, and have this class read settings in
    """

    def __init__(self):
        self.projector_resolution: tuple[int, int] = (1200, 900)
        self.app_resolution: tuple[int, int] = (600, 400)
        self.display = 1
        self.color = {
            "white": "#ffffff",
            "black": "#000000",
            "grey": "#36393f",
            "purple": "#7289da",
        }

    def set_projector_resolution(self, resolution: tuple[int, int]):
        """Set projector resolution tuple (width/height)"""
        self.projector_resolution = resolution

    def set_app_resolution(self, resolution: tuple[int, int]):
        """Set app resolution tuple (width/height)"""
        self.app_resolution = resolution
