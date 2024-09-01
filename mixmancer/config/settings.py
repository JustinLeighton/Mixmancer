import os
from typing import Dict, Any, Optional, Callable, TypeVar, Type
from pathlib import Path

from dotenv import set_key

from mixmancer.config.data_models import Coordinate, Colors
from mixmancer.utils import str_to_coordinate


ENV_FILE = ".env"
T = TypeVar("T")


def set_env_default(key: str) -> str:
    data: Dict[str, str] = {
        "APP_RESOLUTION": "500, 500",
        "PROJECTOR_RESOLUTION": "1280, 900",
        "PROJECTOR_DISPLAY": "1",
        "HEXMAP_PATH": "assets/map/map.png",
        "HEXMAP_OFFSET": "8, 85",
        "HEXMAP_START": "143, 18",
        "HEXMAP_SIZE": "56",
        "COLORS": "#ffffff,#000000,#36393f,#7289da",
    }
    try:
        value = data[key]
        set_env_variable(key, value)
        return value
    except KeyError:
        raise KeyError(f"{key} is not set and does not have a default.")


def get_env_variable(key: str, var_type: Type[T] = str) -> T:
    """Get the value of a specific key from the .env file and convert it to the specified type."""
    value_str: Optional[str] = os.getenv(key.upper(), None)
    if value_str is None:
        value_str = set_env_default(key)

    conversions: Dict[Type[Any], Callable[[str], Any]] = {
        int: lambda x: int(x),
        float: lambda x: float(x),
        bool: lambda x: x.lower() in ("true", "1", "t"),
        list[str]: lambda x: x.split(","),
        Path: lambda x: Path(x),
        Coordinate: str_to_coordinate,
    }

    convert: Callable[[str], T] = conversions.get(var_type, var_type)

    try:
        return convert(value_str)
    except ValueError:
        raise ValueError(f"Cannot convert {value_str} to {var_type.__name__}")


def set_env_variable(key: str, value: Any):
    set_key(ENV_FILE, key.upper(), str(value))


def get_app_resolution() -> Coordinate:
    return get_env_variable("APP_RESOLUTION", Coordinate)


def get_projector_resolution() -> Coordinate:
    return get_env_variable("PROJECTOR_RESOLUTION", Coordinate)


def get_projector_display() -> int:
    return get_env_variable("PROJECTOR_DISPLAY", int)


def get_hexmap_path() -> Path:
    return get_env_variable("HEXMAP_PATH", Path)


def get_hexmap_offset() -> Coordinate:
    return get_env_variable("HEXMAP_OFFSET", Coordinate)


def get_hexmap_start() -> Coordinate:
    return get_env_variable("HEXMAP_START", Coordinate)


def get_hexmap_size() -> int:
    return get_env_variable("HEXMAP_SIZE", int)


def get_colors() -> Colors:
    values = get_env_variable("COLORS", list[str])
    print(values)
    colors = Colors.from_list(values)
    print(colors)
    return Colors.from_list(values)
