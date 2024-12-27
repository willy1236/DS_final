from dataclasses import dataclass
from enum import Enum
from random import choice, randint


class StoneType(Enum):
    TaiwanJade = "豐田玉"
    BlackJade = "墨玉"
    Rhodonite = "玫瑰石"
    GoldenGourdStone = "金瓜石"
    Bloodstone = "雞血石"

stonetype_lst = list(StoneType)

@dataclass(slots=True)
class Stone():
    number: int
    weight: int
    hardness: float
    material: StoneType
    design: str | None
    processing_degree: int

    @classmethod
    def generate(cls, number: int):
        return cls(number, randint(50, 500), randint(55, 70) / 10, choice(stonetype_lst), None, 0)