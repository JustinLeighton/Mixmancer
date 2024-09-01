from pydantic import BaseModel, field_validator
from typing import Any, Tuple, List
import re


class DataModel(BaseModel):
    d4: int
    d6: int
    d8: int
    d10: int
    d12: int
    d20: int
    d100: int
    modifier: int
    advantage: bool
    disadvantage: bool


class Colors(BaseModel):
    white: str
    black: str
    grey: str
    purple: str

    @field_validator("white", "black", "grey", "purple")
    def check_color(cls, v: str) -> str:
        if not re.match(r"^#[0-9a-fA-F]{6}$", v):
            raise ValueError(f"Invalid color value: {v}. Must be a valid hex color code.")
        return v

    @classmethod
    def from_list(cls, values: List[str]) -> "Colors":
        if len(values) != 4:
            raise ValueError("Expected 4 color values")
        return cls(white=values[0], black=values[1], grey=values[2], purple=values[3])


class Coordinate(BaseModel):
    x: int
    y: int

    def __init__(self, x: int, y: int):
        super().__init__(x=x, y=y)

    def __call__(self) -> Tuple[int, int]:
        return (self.x, self.y)

    def __repr__(self) -> str:
        return f"Coordinate(x={self.x}, y={self.y})"

    def __str__(self) -> str:
        return f"{self.x},{self.y}"

    def __add__(self, other: "Coordinate") -> "Coordinate":
        return Coordinate(x=self.x + other.x, y=self.y + other.y)

    def __sub__(self, other: "Coordinate") -> "Coordinate":
        return Coordinate(x=self.x - other.x, y=self.y - other.y)

    def __mul__(self, other: "Coordinate") -> "Coordinate":
        return Coordinate(x=self.x * other.x, y=self.y * other.y)

    def __truediv__(self, constant: float) -> "Coordinate":
        if constant == 0:
            raise ValueError("Cannot divide by zero")
        return Coordinate(x=int(self.x / constant), y=int(self.y / constant))

    def __floordiv__(self, constant: int) -> "Coordinate":
        if constant == 0:
            raise ValueError("Cannot divide by zero")
        return Coordinate(x=self.x // constant, y=self.y // constant)

    def float(self) -> tuple[float, float]:
        return (float(self.x), float(self.y))

    def half(self) -> Tuple[int, int]:
        return (self.x // 2, self.y // 2)

    @field_validator("x", "y")  # type: ignore
    def check_integer(cls, v: Any) -> int:
        if not isinstance(v, int):
            raise ValueError(f"Value must be int, got {type(v).__name__}")
        return v
