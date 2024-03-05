import pytest
import pygame
import math
import os
from mixmancer.display.hexmap import HexMap


@pytest.fixture
def hex_map():
    return HexMap(
        image_path="assets/tests/test_wide.jpg",
        resolution=(600, 400),
        hex_size=20,
        offset=(1, 2),
        start_coordinates=(10, 12),
    )


def test_initialization(hex_map: HexMap):
    assert isinstance(hex_map.image, pygame.Surface)
    assert hex_map.resolution == [600, 400]
    assert hex_map.hex_size == 20
    assert hex_map.offset == [1, 2]
    assert hex_map.location_grid == (10, 12)
    assert hex_map.stagger is True
    assert not hex_map.fog_flag
    assert not hex_map.history_flag
    assert hex_map.yellow == (255, 215, 0)


def test_check_stagger(hex_map: HexMap):
    assert hex_map.check_stagger((0, 0)) == True
    assert hex_map.check_stagger((1, 0)) == False


def test_frame(hex_map: HexMap):
    x, y = hex_map.frame()
    assert math.floor(x) == -41.0
    assert math.floor(y) == 124.0


def test_grid_to_pixel(hex_map: HexMap):
    x, y = hex_map.grid_to_pixel((0, 0))
    assert math.floor(x) == 2
    assert math.floor(y) == 1
    x, y = hex_map.grid_to_pixel((1, 0))
    assert math.floor(x) == 19
    assert math.floor(y) == -9


def test_update(hex_map: HexMap):
    hex_map.update()
    assert hex_map.stagger is not None
    assert isinstance(hex_map.location_pixel, tuple)
    assert len(hex_map.location_pixel) == 2
    assert isinstance(hex_map.location_pixel[0], float)
    assert isinstance(hex_map.location_pixel[1], float)


def test_hex_points(hex_map: HexMap):
    points = hex_map.hex_points()
    assert len(points) == 7
    for point in points:
        assert isinstance(point, tuple)
        assert len(point) == 2
        assert isinstance(point[0], float)
        assert isinstance(point[1], float)


def test_check_on_screen(hex_map: HexMap):
    assert hex_map.check_on_screen((0, 0)) == True
    assert hex_map.check_on_screen((500, 700)) == False


def test_normalize_pixel_location(hex_map: HexMap):
    normalized = hex_map.normalize_pixel_location((200, 200))
    assert isinstance(normalized, tuple)
    assert len(normalized) == 2
    assert isinstance(normalized[0], float)
    assert isinstance(normalized[1], float)


def test_read_history(hex_map: HexMap):
    history_file = "assets/tests/history.txt"
    hex_map.history_file = history_file
    hex_map.reset_history()
    with open(history_file, "w") as file:
        file.write("0,0\n1,1\n2,2\n")
    hex_map.read_history(history_file)
    assert hex_map.read_history(history_file) == [(0, 0), (1, 1), (2, 2)]


def test_log_movement(hex_map: HexMap):
    history_file = "assets/tests/history.txt"
    hex_map.history_file = history_file
    hex_map.reset_history()
    hex_map.log_movement()
    assert hex_map.read_history(history_file) == [(10, 12)]


def test_reset_history(hex_map: HexMap):
    history_file = "assets/tests/history.txt"
    hex_map.history_file = history_file
    hex_map.log_movement()
    hex_map.reset_history()
    assert hex_map.read_history(history_file) == []


def test_get_direction_mapping(hex_map: HexMap):
    mapping = hex_map.get_direction_mapping()
    assert isinstance(mapping, dict)
    assert len(mapping) == 6
    for _, value in mapping.items():
        assert callable(value)


def test_toggle_history_flag(hex_map: HexMap):
    initial_flag = hex_map.history_flag
    hex_map.toggle_history_flag()
    assert hex_map.history_flag == (not initial_flag)


def test_toggle_fog_flag(hex_map: HexMap):
    initial_flag = hex_map.fog_flag
    hex_map.toggle_fog_flag()
    assert hex_map.fog_flag == (not initial_flag)


def test_move(hex_map: HexMap):
    initial_location = hex_map.location_grid
    hex_map.move((-1, 1))
    assert hex_map.location_grid == (initial_location[0] - 1, initial_location[1] + 1)


def test_command(hex_map: HexMap):
    initial_location = hex_map.location_grid
    hex_map.command("Upper Right")
    assert hex_map.location_grid == (initial_location[0] - 1, initial_location[1] + 1)


def test_dump(hex_map: HexMap):
    temp_file = hex_map.dump()
    assert os.path.exists(temp_file)
