import pygame


class ImageProjector:
    """
    A class to manage images projected to second display

    Attributes:
        resolution (tuple): A tuple representing the resolution of the display.
        display (int): An integer representing the display number.
        screen (pygame.Surface): A Pygame Surface object representing the screen.
        status (bool): A boolean indicating the status of the projector.
        image (pygame.Surface): A Pygame Surface object representing the loaded image.
    """

    def __init__(self, resolution: tuple[int, int], display: int):
        """
        Initializes the ImageProjector object with the given resolution and display.

        Args:
            resolution (tuple): A tuple representing the resolution of the display.
            display (int): An integer representing the display number.
        """
        self.resolution = resolution
        self.screen = pygame.display.set_mode(resolution, flags=pygame.NOFRAME, display=display)
        self.status = False
        self.image: pygame.Surface

    def load_image(self, image: str):
        """
        Loads an image onto the projector.

        Args:
            image (str): The file path of the image to be loaded.
        """
        try:
            self.image = pygame.image.load(image)
            self.blit()
            return True
        except:
            return False

    def blit(self):
        """
        Blits the loaded image onto the screen. Auto-sizes image depending on screen resolution.
        """
        self.screen.fill((0, 0, 0))
        sw, sh = self.resolution
        iw, ih = self.image.get_width(), self.image.get_height()
        if iw / ih > sw / sh:
            t = sw / iw
        else:
            t = sh / ih
        self.image = pygame.transform.scale(self.image, (t * iw, t * ih))
        self.screen.blit(self.image, ((sw - t * iw) / 2, (sh - t * ih) / 2))
        pygame.display.update()
