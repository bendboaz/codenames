from enum import Enum, auto

from typing import NamedTuple


class Coordinate(NamedTuple):
    x: int
    y: int


class Clue(NamedTuple):
    clue: str
    num_guesses: int


class AgentType(Enum):
    RED = auto()
    BLUE = auto()
    BLACK = auto()
    INNOCENT = auto()


class GameStatus(Enum):
    INITIALIZED = "initialized"
    RUNNING = "running"
    DONE = "done"


class GameEndStatus(Enum):
    RED_VICTORY = "RED_VICTORY"
    BLUE_VICTORY = "BLUE_VICTORY"
    BLACK_REVEALED = "BLACK_REVEALED"
    ONGOING = "ONGOING"
