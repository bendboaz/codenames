import uuid
from typing import Literal, TYPE_CHECKING, Optional

from pydantic import BaseModel

from app.bll.board import Board
from app.bll.defaults import DEFAULT_BOARD_SIZE
from app.bll.types import GameStatus, GameEndStatus, AgentType, GameState, Clue

if TYPE_CHECKING:
    from app.dal.base_data_access import BaseDataAccess


class InvalidGuessException(Exception):
    """Exception raised for invalid guesses during the game."""

    pass


class CurrentTurnState(BaseModel):
    player: Literal[AgentType.RED] | Literal[AgentType.BLUE]
    clue: Optional[Clue] = None
    guesses_made: int = 0


class Game(BaseModel):
    game_id: str
    board: Board
    status: GameStatus
    game_end_status: GameEndStatus
    current_turn: CurrentTurnState

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @classmethod
    def new_game(cls, words_provider: "BaseDataAccess"):
        board = Board.random_with_words(
            words_provider.load_card_words()[:DEFAULT_BOARD_SIZE]
        )
        return cls(
            game_id=str(uuid.uuid4()),
            board=board,
            status=GameStatus.INITIALIZED,
            game_end_status=GameEndStatus.ONGOING,
        )

    def get_state(self) -> GameState:
        words = self.board.words
        current_player = self.current_player
        victory_state = self.game_end_status
        return GameState(words, current_player, victory_state)
