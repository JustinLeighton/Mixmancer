import pygame
import math
from PIL import Image
from mixmancer.config.data_models import Coordinate


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
        self.update_parameters(hex_size, offset, start_coordinates)
        self.fog_flag = False
        self.history_flag = False
        self.yellow = (255, 215, 0)
        self.history_file: str = "./assets/map/history.txt"

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
        print(
            f"""
            location_grid: {self.location_grid}
            location_pixel: {self.location_pixel} 
            stagger: {self.stagger}
            hex_size: {self.hex_size}
            side_length: {self.side_length}
            """
        )

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
        x = int(grid_location.x * self.hex_size * 2 + self.offset.x)
        y = int(grid_location.y * self.side_length * 2 + self.offset.y)
        # int(grid_location.y * self.side_length * 1.5 + self.offset.y)
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

        # Use pygame rect collide
        # for i in (0, 1):
        #     if (
        #         pixel_coordinates[i] > self.location_pixel[i] + self.resolution[::-1][i] / 2
        #         or pixel_coordinates[i] < self.location_pixel[i] - self.resolution[::-1][i] / 2
        #     ):
        #         return False
        return True

    def normalize_pixel_location(self, pixel_coordinates: Coordinate) -> Coordinate:
        """Normalize pixel coordinates given a screen frame centered on the player's frame of reference.

        Args:
            pixel_coordinates (Coordinate): The pixel coordinates (x, y).

        Returns:
            Coordinate: The normalized pixel coordinates (x, y).
        """
        return (pixel_coordinates - self.location_pixel + self.resolution).divide(2)

    def get_history(self) -> list[Coordinate]:
        """Get a list of historical grid points and convert to pixel coordinates.

        Returns:
            list[Coordinate]: List of historical pixel coordinates.
        """
        output: list[Coordinate] = []
        for grid_coordinate in self.read_history(self.history_file):
            pixel_coordinate = self.grid_to_pixel(grid_coordinate)
            if self.check_on_screen(pixel_coordinate):
                output.append(pixel_coordinate)
        return output

    def read_history(self, file_location: str) -> list[Coordinate]:
        """Read historical grid coordinates from file.

        Returns:
            list[Coordinate]: List of historical grid coordinates.
        """
        with open(file_location, "r") as file:
            data: list[Coordinate] = []
            for line in file:
                try:
                    y, x = map(int, line.strip().split(","))
                    data.append(Coordinate(y, x))
                except ValueError as e:
                    raise ValueError(f"Error converting line '{line.strip()}' to int: {e}")
        return data

    def undo_movement(self):
        """Undo the last movement."""
        data = self.read_history(self.history_file)
        data = data[:-1]
        self.location_grid = data[len(data) - 1]
        with open(self.history_file, "w") as f:
            f.writelines(",".join(map(str, x)) + "\n" for x in data)
        self.update()

    def log_movement(self):
        """Log the last movement in the history file."""
        with open(self.history_file, "a") as f:
            f.write(f"{','.join([str(x) for x in self.location_grid])}\n")

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

    def toggle_fog_flag(self):
        """Toggle the fog flag. This allows the user to enable or disable fog to obscure unexplored areas of the map. - UNFINISHED"""
        self.fog_flag = not self.fog_flag

    def move(self, direction: Coordinate):
        """Move the player across the map in a specified direction.

        Args:
            direction (Coordinate): The direction to move (x, y) in grid coordinate.
        """
        self.location_grid += direction

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
