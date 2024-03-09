from pathlib import Path
import os


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


def calculate_resized_dimensions(image_dimensions: tuple[int, int], target_location: tuple[int, int]):
    """Calculate the resized dimensions of an image while maintaining aspect ratio,
    maximizing the space within the target location.

    Args:
    - image_dimensions (tuple): Dimensions of the original image (width, height).
    - target_location (tuple): Planned location of the image (x, y) within its container.

    Returns:
    - tuple: Resized dimensions (width, height).
    """
    # Unpack image dimensions
    image_width: int
    image_height: int
    available_width: int
    available_height: int
    image_width, image_height = image_dimensions
    available_width, available_height = target_location

    # Calculate aspect ratio of the original image
    try:
        aspect_ratio = image_width / image_height
    except ZeroDivisionError as e:
        raise ZeroDivisionError("Cannot calculate aspect ratio: Image height cannot be zero") from e

    # Calculate new dimensions while maintaining aspect ratio
    if available_width / aspect_ratio <= available_height:
        new_width = available_width
        new_height = int(new_width / aspect_ratio)
    else:
        new_height = available_height
        new_width = int(new_height * aspect_ratio)
    return new_width, new_height
