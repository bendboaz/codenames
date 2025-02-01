from enum import Enum

from typing import Literal, Optional

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


class GameEndStatus(Enum):
    RED_VICTORY = "RED_VICTORY"
    BLUE_VICTORY = "BLUE_VICTORY"
    BLACK_REVEALED = "BLACK_REVEALED"
    ONGOING = "ONGOING"


class Card(BaseModel):
    word: str
    card_type: AgentType


TeamColor = Literal[AgentType.RED] | Literal[AgentType.BLUE]


class CurrentTurnState(BaseModel):
    team: TeamColor
    clue: Optional[Clue] = None
    guesses_made: int = 0


class GameState(BaseModel):
    game_id: str
    words: list[list[Card]]
    current_turn: CurrentTurnState
    victory_state: GameEndStatus
