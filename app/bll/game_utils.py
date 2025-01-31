import itertools
from typing import TypeVar

from app.bll.defaults import DEFAULT_BOARD_SIZE

BOARD_CONTENT_TYPE = TypeVar("BOARD_CONTENT_TYPE")


def get_empty_board(
    board_size: int = DEFAULT_BOARD_SIZE, empty_value: BOARD_CONTENT_TYPE = ""
) -> list[list[BOARD_CONTENT_TYPE]]:
    return [list(itertools.repeat(empty_value, board_size)) for _ in range(board_size)]
