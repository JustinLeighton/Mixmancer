from pydantic import BaseModel


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
