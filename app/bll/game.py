import uuid
from pathlib import Path
from typing import Literal

from pydantic import BaseModel

from app.bll.board import Board
from app.bll.defaults import DEFAULT_BOARD_SIZE
from app.bll.types import GameStatus, GameEndStatus, AgentType, GameState
from app.dal.local_dal import LocalDataAccess


class Game(BaseModel):
    id: str
    board: Board
    status: GameStatus
    game_end_status: GameEndStatus
    current_player: Literal[AgentType.RED] | Literal[AgentType.BLUE]

    def __init__(
        self,
        game_id: str,
        board: Board,
        status: GameStatus,
        game_end_status: GameEndStatus,
        current_player: Literal[AgentType.RED] | Literal[AgentType.BLUE] | None,
    ):
        super().__init__()

        self.id = game_id
        self.board = board
        self.status = status
        self.game_end_status = game_end_status
        self.current_player = (
            current_player
            if current_player is not None
            else self.board.agent_placements.starting_color
        )

    @classmethod
    def new_game(cls):
        words_provider = LocalDataAccess(Path("data"))
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
