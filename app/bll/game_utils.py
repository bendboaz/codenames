import itertools
from typing import TypeVar

from app.bll.defaults import DEFAULT_BOARD_SIZE
from app.bll.types import Player, AgentType

BOARD_CONTENT_TYPE = TypeVar("BOARD_CONTENT_TYPE")


def get_empty_board(
    board_size: int = DEFAULT_BOARD_SIZE, empty_value: BOARD_CONTENT_TYPE = ""
) -> list[list[BOARD_CONTENT_TYPE]]:
    return [list(itertools.repeat(empty_value, board_size)) for _ in range(board_size)]


def change_player(player: Player) -> Player:
    if player not in [AgentType.RED, AgentType.BLUE]:
        raise ValueError(
            f"Can only switch between {AgentType.RED} and {AgentType.BLUE} players, got {player}"
        )

    return AgentType.BLUE if player == AgentType.RED else AgentType.RED
