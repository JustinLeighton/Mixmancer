from pydantic import BaseModel, field_validator
from typing import Any, Tuple


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


class Coordinate(BaseModel):
    x: int
    y: int

    def __init__(self, x: int, y: int):
        super().__init__(x=x, y=y)

    def __call__(self) -> Tuple[int, int]:
        return (self.x, self.y)

    def __repr__(self) -> str:
        return f"Coordinate(x={self.x}, y={self.y})"

    def __add__(self, other: "Coordinate") -> "Coordinate":
        return Coordinate(x=self.x + other.x, y=self.y + other.y)

    def __sub__(self, other: "Coordinate") -> "Coordinate":
        return Coordinate(x=self.x - other.x, y=self.y - other.y)

    def __mul__(self, other: "Coordinate") -> "Coordinate":
        return Coordinate(x=self.x * other.x, y=self.y * other.y)

    def divide(self, constant: float) -> "Coordinate":
        if constant == 0:
            raise ValueError("Cannot divide by zero")
        return Coordinate(x=int(self.x / constant), y=int(self.y / constant))

    def float(self) -> tuple[float, float]:
        return (float(self.x), float(self.y))

    def half(self) -> Tuple[int, int]:
        return (self.x // 2, self.y // 2)

    @field_validator("x", "y")  # type: ignore
    def check_integer(cls, v: Any) -> int:
        if not isinstance(v, int):
            raise ValueError(f"Value must be int, got {type(v).__name__}")
        return v
