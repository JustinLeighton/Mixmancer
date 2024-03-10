import pygame
from PIL import Image
import os


class ImageProjector:
    """A class to manage images projected to second display

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
        self.image: pygame.Surface = None  # type: ignore[reportAttributeAccessIssue]
        self.current_image: str = ""

    def load_image_file(self, image_file: str) -> bool:
        """Loads an image from file into the projector.

        Args:
            image_file (str): The file path of the image to be loaded.

        Returns:
            bool: True if successful, False if unsuccessful
        """
        try:
            self.image = pygame.image.load(image_file)
            self.blit()
            self.set_current_image(os.path.basename(image_file))
            return True
        except:
            return False

    def load_image_pil(self, image_pil: Image.Image) -> bool:
        """Loads a PIL Image object into the projector.

        Args:
            image_pil (Image.Image): The object being loaded

        Returns:
            bool: True if successful, False if unsuccessful
        """
        try:
            image_data = image_pil.tobytes()  # type: ignore[reportUnknownMemberType]
            self.image = pygame.image.frombuffer(image_data, image_pil.size, image_pil.mode)  # type: ignore[reportArgumentType]
            self.blit()
            self.set_current_image("hexmap")
            return True
        except:
            return False

    def set_current_image(self, image_name: str):
        """Set the name of the current image loaded"""
        self.current_image = image_name

    def get_current_image(self, max_length: int = 15) -> str:
        """Get the name of the current image loaded"""
        file_name = os.path.basename(self.current_image)
        if len(file_name) > max_length:
            return file_name[:max_length] + "..."
        return file_name

    def get_image_pil(self) -> Image.Image:
        """Get PIL image object from pygame display"""
        bytes_data = pygame.image.tostring(self.image, "RGBA")
        image_pil = Image.frombytes("RGBA", self.image.get_size(), bytes_data)  # type: ignore[reportUnknownMemberType]
        return image_pil

    def blit(self):
        """Blits the loaded image onto the screen. Auto-sizes image depending on screen resolution."""
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
