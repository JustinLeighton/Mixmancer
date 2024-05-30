from pathlib import Path
import os
from mixmancer.config.data_models import Coordinate


def check_file_exists(file_path: str) -> bool:
    """Check if a file exists.

    Args:
        file_path (Union[str, Path]): The path to the file.
    """
    try:
        file_path = Path(file_path)  # type: ignore[reportAssignmentType]
    except TypeError as e:
        print("File path must be a string or Path object", e)
        return False

    try:
        if not file_path.exists():  # type: ignore
            raise FileNotFoundError(f"File '{file_path}' does not exist")
    except FileNotFoundError as e:
        print(e)
        return False

    try:
        if not os.access(file_path, os.R_OK):
            raise PermissionError(f"No read access to file '{file_path}'")
    except PermissionError as e:
        print(e)
        return False

    return True


def calculate_resized_dimensions(image_dimensions: Coordinate, target_location: Coordinate) -> Coordinate:
    """Calculate the resized dimensions of an image while maintaining aspect ratio,
    maximizing the space within the target location.

    Args:
    - image_dimensions (Coordinate): Dimensions of the original image (width, height).
    - target_location (Coordinate): Planned location of the image (x, y) within its container.

    Returns:
    - Coordinate: Resized dimensions (width, height).
    """
    # Calculate aspect ratio of the original image
    try:
        aspect_ratio = image_dimensions.x / image_dimensions.y
    except ZeroDivisionError as e:
        raise ZeroDivisionError("Cannot calculate aspect ratio: Image height cannot be zero") from e

    # Calculate new dimensions while maintaining aspect ratio
    if target_location.x / aspect_ratio <= target_location.y:
        return Coordinate(target_location.x, int(target_location.x / aspect_ratio))
    else:
        return Coordinate(int(target_location.y * aspect_ratio), target_location.y)
