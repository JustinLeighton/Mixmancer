import pygame
import math
from PIL import Image
from numpy import arange, linspace, float_
from numpy.typing import NDArray
from mixmancer.config.data_models import Coordinate

from scipy import interpolate  # type: ignore[reportMissingTypeStubs]


class HexMap:
    """Hexmap object. Displays a hexagonal map and allows for movement and exploration.

    Attributes:
        image (pygame.Surface): The image representing the map.
        resolution (Coordinate): The resolution of the map.
        hex_size (int): The size of each hexagon in pixels.
        offset (Coordinate): The offset of the map.
        location_grid (Coordinate): The current location on the grid.
        location_pixel (Coordinate): The current location in pixels.
        side_length (float): The length of each side of a hexagon.
        fog_flag (bool): Flag indicating whether fog is enabled.
        history_flag (bool): Flag indicating whether history is being shown.
        yellow (tuple[int, int, int]): RGB tuple representing the color yellow.
        stagger (bool): Flag indicating whether staggered hex layout is used.
        history_file (str): path to text log of past player movement
    """

    def __init__(
        self,
        image_path: str,
        resolution: Coordinate,
        hex_size: int,
        offset: Coordinate,
        start_coordinates: Coordinate,
    ):
        """
        Initialize the HexMap object.

        Args:
            image_path (str): The file path to the image representing the map.
            resolution (Coordinate): The resolution of the map (width, height).
            hex_size (int): The size of each hexagon in pixels.
            offset (Coordinate): The offset of the map (x, y).
            start_coordinates (Coordinate): The starting coordinates on the grid (row, column).
        """
        self.image = pygame.image.load(image_path)
        self.resolution = resolution
        self.location_pixel: Coordinate
        self.stagger: bool
        self.fog_flag = False
        self.history_flag = False
        self.yellow = (255, 215, 0)
        self.history_file: str = "./assets/map/history.txt"
        data = self.read_history(self.history_file)
        if data:
            start_coordinates = data[-1]
        self.update_parameters(hex_size, offset, start_coordinates)

    def update_parameters(self, hex_size: int, offset: Coordinate, location_grid: Coordinate):
        self.hex_size = hex_size
        self.offset = offset
        self.location_grid = location_grid
        self.side_length: float = 2 * ((self.hex_size / 2) / math.tan(math.pi / 3))
        self.update()

    def update(self):
        """Update pixel location and stagger bool according to the player location on the map."""
        self.stagger = self.check_stagger(self.location_grid)
        self.location_pixel = self.grid_to_pixel(self.location_grid)

    def check_stagger(self, grid_location: Coordinate) -> bool:
        """Check if current location is on a staggered hex row or not.

        Args:
            grid_location (Coordinate): The grid location (row, column).

        Returns:
            bool: True if staggered layout is used, False otherwise.
        """
        return grid_location.y % 2 == 0  # True = 1-3-3, False = 3-3-1

    def frame(self) -> tuple[int, ...]:
        """Calculate the center of the screen from the pixel location of the player"""
        center = self.resolution - self.location_pixel
        return center.half()

    def reset_history(self):
        """Reset player movement text log file"""
        with open(self.history_file, "w") as file:
            file.truncate(0)

    def grid_to_pixel(self, grid_location: Coordinate) -> Coordinate:
        """Convert grid coordinates to pixel coordinates.

        Args:
            grid_location (Coordinate): The grid location (row, column).

        Returns:
            Coordinate: The pixel coordinates (x, y).
        """
        y = 2 * int(grid_location.y * self.side_length * 1.5 + self.offset.y)
        x = 2 * int(
            grid_location.x * self.hex_size
            + self.offset.x
            - (not self.check_stagger(grid_location)) * 0.5 * self.hex_size
        )
        return Coordinate(x, y)

    def hex_points(self):
        """Calculate the points of a hexagon to indicate the players location."""
        x, y = self.resolution.divide(2)()
        pad = 1
        return [
            (x - self.hex_size / 2 - pad, y - self.side_length / 2 - pad),
            (x, y - self.side_length - pad),
            (x + self.hex_size / 2 + pad, y - self.side_length / 2 - pad),
            (x + self.hex_size / 2 + pad, y + self.side_length / 2 - pad),
            (x, y + self.side_length),
            (x - self.hex_size / 2 - pad, y + self.side_length / 2 - pad),
            (x - self.hex_size / 2 - pad, y - self.side_length / 2 - pad),
        ]

    def check_on_screen(self, pixel_coordinates: Coordinate) -> bool:
        """Check if given pixel coordinates are on the screen.

        Args:
            pixel_coordinates (Coordinate): The pixel coordinates (x, y).

        Returns:
            bool: True if on screen, False otherwise.
        """
        screen = pygame.Rect(*(self.location_pixel - self.resolution.divide(2))(), *self.resolution())
        return pygame.Rect(pixel_coordinates()).colliderect(screen)

    def normalize_pixel_location(self, pixel_coordinates: Coordinate) -> Coordinate:
        """Normalize pixel coordinates given a screen frame centered on the player's frame of reference.

        Args:
            pixel_coordinates (Coordinate): The pixel coordinates (x, y).

        Returns:
            Coordinate: The normalized pixel coordinates (x, y).
        """
        return (pixel_coordinates - self.location_pixel + self.resolution).divide(2)

    def read_history(self, file_location: str) -> list[Coordinate]:
        """Read historical grid coordinates from file.

        Returns:
            list[Coordinate]: List of historical grid coordinates.
        """
        with open(file_location, "r") as file:
            data: list[Coordinate] = []
            for line in file:
                try:
                    x, y = map(int, line.strip().split(","))
                    data.append(Coordinate(x, y))
                except ValueError as e:
                    raise ValueError(f"Error converting line '{line.strip()}' to int: {e}")
        return data

    def undo_movement(self):
        """Undo the last movement."""
        data = self.read_history(self.history_file)
        data = data[:-1]
        self.location_grid = data[len(data) - 1]
        with open(self.history_file, "w") as f:
            f.writelines(",".join(map(str, x())) + "\n" for x in data)
        self.update()

    def log_movement(self):
        """Log the last movement in the history file."""
        with open(self.history_file, "a") as f:
            f.write(f"{','.join([str(x) for x in self.location_grid()])}\n")

    def get_direction_mapping(self):
        """Translate direction into grid point coordinates with respect to the staggered grid layout."""
        mapping = {
            "upper_right": lambda: self.move(Coordinate(1 if self.stagger else 0, -1)),
            "upper_left": lambda: self.move(Coordinate(-1 if not self.stagger else 0, -1)),
            "right": lambda: self.move(Coordinate(1, 0)),
            "left": lambda: self.move(Coordinate(-1, 0)),
            "lower_right": lambda: self.move(Coordinate(1 if self.stagger else 0, 1)),
            "lower_left": lambda: self.move(Coordinate(-1 if not self.stagger else 0, 1)),
        }
        return mapping

    def toggle_history_flag(self):
        """Toggle the history flag. This allows the user to enable or disable lines showing historical movement across the map - UNFINISHED"""
        self.history_flag = not self.history_flag
        self.update()

    def toggle_fog_flag(self):
        """Toggle the fog flag. This allows the user to enable or disable fog to obscure unexplored areas of the map. - UNFINISHED"""
        self.fog_flag = not self.fog_flag

    def move(self, direction: Coordinate):
        """Move the player across the map in a specified direction.

        Args:
            direction (Coordinate): The direction to move (x, y) in grid coordinate.
        """
        self.location_grid += direction
        self.log_movement()

    def command(self, command: str):
        """Execute a command. This routes all possible inputs from the tkinter widgets to the HexMap object.

        Args:
            command (str): The command to execute.
        """

        command_actions = {
            "undo": self.undo_movement,
            "history": self.toggle_history_flag,
            "fog": self.toggle_fog_flag,
            **self.get_direction_mapping(),
        }

        action = command_actions.get(command)
        if action:
            action()
            self.update()

    def get_current_surface(self) -> pygame.Surface:
        """Get the current playing surface of the hexmap

        Returns:
            pygame.Surface: The current cropped map centered on player location
        """
        surface = pygame.Surface((self.resolution.x, self.resolution.y))
        surface.fill((0, 0, 0))
        surface.blit(self.image, self.frame())

        # Draw current location
        pygame.draw.polygon(surface, color=self.yellow, points=self.hex_points(), width=3)

        # Draw history
        if self.history_flag:
            data = self.read_history(self.history_file)
            normalized_points = [self.normalize_pixel_location(self.grid_to_pixel(pt)).float() for pt in data]
            x = [pt[0] for pt in normalized_points]
            y = [pt[1] for pt in normalized_points]
            draw_spline_curve(surface, self.yellow, x, y)

        # Draw fog
        if self.fog_flag:
            pass

        return surface

    def get_current_surface_PIL(self) -> Image.Image:
        """Convert pygame surface to PIL image object"""
        surface = self.get_current_surface()
        image_data = pygame.image.tostring(surface, "RGBA")
        image_pil = Image.frombytes("RGBA", surface.get_size(), image_data)  # type: ignore[reportUnknownMemberType]
        return image_pil

    def dump(self) -> str:
        """Dump an image of the current frame of the map image."""
        temp_file = "./assets/map/tmp.png"
        surface = self.get_current_surface()
        pygame.image.save(surface, temp_file)
        return temp_file


def interpolate_curve(
    x: list[float], y: list[float], num_points: int = 1000
) -> tuple[NDArray[float_], NDArray[float_]]:
    spline_x = interpolate.UnivariateSpline(arange(len(x)), x, s=0)
    spline_y = interpolate.UnivariateSpline(arange(len(y)), y, s=0)
    u = linspace(0, len(x) - 1, num_points)
    xi = spline_x(u)  # type: ignore
    yi = spline_y(u)  # type: ignore
    return xi, yi  # type: ignore


def draw_spline_curve(
    surface: pygame.Surface,
    color: tuple[int, int, int],
    x: list[float],
    y: list[float],
    num_points: int = 1000,
    width: int = 2,
) -> None:
    xi, yi = interpolate_curve(x, y, num_points)
    points = list(zip(xi, yi))
    pygame.draw.lines(surface, color, False, points, width)
