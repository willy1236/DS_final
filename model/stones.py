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

@dataclass
class Stone():
    number: int
    length: int
    width: int
    height: int
    weight: int
    material: StoneType

    @classmethod
    def generate(cls, number: int):
        return cls(number, randint(5, 20), randint(5, 20), randint(5, 20), randint(50, 1000), choice(stonetype_lst))