class Settings:
    """
    Object to hold app settings. Plan to move this into json, and have this class read settings in
    """

    def __init__(self):
        self.projector_width = 1200
        self.projector_height = 900
        self.app_width = 600
        self.app_height = 400
        self.display = 1
        self.color = {
            "white": "#ffffff",
            "black": "#000000",
            "grey": "#36393f",
            "purple": "#7289da",
        }
