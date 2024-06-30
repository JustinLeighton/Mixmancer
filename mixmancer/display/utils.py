import pygame
from typing import Optional


def resize_image_with_aspect_ratio(
    image: pygame.Surface, width: Optional[int] = None, height: Optional[int] = None
) -> pygame.Surface:
    """
    Resizes an image while maintaining its aspect ratio.

    Args:
        image (pygame.Surface): The original image to be resized.
        width (Optional[int]): The desired width of the resized image. If None, the width is calculated based on the height.
        height (Optional[int]): The desired height of the resized image. If None, the height is calculated based on the width.

    Returns:
        pygame.Surface: The resized image with the original aspect ratio maintained.
    """
    # Get the original dimensions of the image
    original_width, original_height = image.get_size()

    # If both width and height are None, return the original image
    if width is None and height is None:
        return image

    # If only width is specified, calculate the height to keep the aspect ratio
    if width is not None and height is None:
        aspect_ratio = original_height / original_width
        height = int(width * aspect_ratio)

    # If only height is specified, calculate the width to keep the aspect ratio
    if height is not None and width is None:
        aspect_ratio = original_width / original_height
        width = int(height * aspect_ratio)

    # Resize the image
    resized_image = pygame.transform.scale(image, (width, height))  # type: ignore[reportArgumentType]

    return resized_image
