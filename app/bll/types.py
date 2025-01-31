from enum import Enum

from typing import Literal

from pydantic import BaseModel


class Coordinate(BaseModel):
    x: int
    y: int

    @classmethod
    def from_tuple(cls, *tup: [int, int]):
        x, y = tup
        return cls(x=x, y=y)


class Clue(BaseModel):
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


class Card(BaseModel):
    word: str
    card_type: AgentType


class GameState(BaseModel):
    game_id: str
    words: list[list[Card]]
    current_player: Literal[AgentType.RED] | Literal[AgentType.BLUE]
    victory_state: GameEndStatus
