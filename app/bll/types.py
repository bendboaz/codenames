from enum import Enum

from typing import NamedTuple, Literal


class Coordinate(NamedTuple):
    x: int
    y: int


class Clue(NamedTuple):
    clue: str
    num_guesses: int


class AgentType(Enum):
    RED = "RED"
    BLUE = "BLUE"
    BLACK = "BLACK"
    INNOCENT = "INNOCENT"
    UNKNOWN = "UNKNOWN"


class GameStatus(Enum):
    INITIALIZED = "initialized"
    RUNNING = "running"
    DONE = "done"


class GameEndStatus(Enum):
    RED_VICTORY = "RED_VICTORY"
    BLUE_VICTORY = "BLUE_VICTORY"
    BLACK_REVEALED = "BLACK_REVEALED"
    ONGOING = "ONGOING"


class Card(NamedTuple):
    word: str
    card_type: AgentType


class GameState(NamedTuple):
    words: list[list[Card]]
    current_player: Literal[AgentType.RED] | Literal[AgentType.BLUE]
    victory_state: GameEndStatus
