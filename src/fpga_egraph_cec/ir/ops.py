from enum import Enum, auto


class Op(Enum):
    INPUT = auto()
    CONST0 = auto()
    CONST1 = auto()
    NOT = auto()
    AND = auto()
    OR = auto()
    XOR = auto()
    MUX = auto()