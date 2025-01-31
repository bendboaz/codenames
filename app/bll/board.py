from dataclasses import Field

from pydantic import BaseModel

from app.bll.game_utils import get_empty_board
from app.bll.types import AgentType, Coordinate


class AgentPlacements(BaseModel):
    positions: dict[AgentType, list[Coordinate]]
    starting_color: AgentType
    _shadow_board: list[list[AgentType]] = Field(default_factory=lambda: AgentPlacements.build_shadow_board_static())

    @staticmethod
    def build_shadow_board_static(positions: dict[AgentType, list[Coordinate]] = {}) -> list[list[AgentType]]:
        shadow_board = get_empty_board(empty_value=AgentType.INNOCENT)
        for agent, coordinates in positions.items():
            for coord in coordinates:
                shadow_board[coord.x][coord.y] = agent
        return shadow_board

    def __getitem__(self, item: Coordinate) -> AgentType:
        return self._shadow_board[item.x][item.y]


class Board(BaseModel):
    cards: list[list[str]]
    discovered_agents: list[Coordinate]
    agent_placements: AgentPlacements
