import itertools
import random
from copy import deepcopy
from typing import Optional

from pydantic import BaseModel, Field

from app.bll.defaults import DEFAULT_BOARD_SIZE
from app.bll.game_utils import get_empty_board
from app.bll.types import AgentType, Coordinate


class AgentPlacements(BaseModel):
    positions: dict[AgentType, list[Coordinate]]
    starting_color: AgentType
    shadow_board: list[list[AgentType]] = Field(
        default_factory=lambda: get_empty_board(empty_value=AgentType.INNOCENT)
    )

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.build_shadow_board_static()

    def build_shadow_board_static(self) -> list[list[AgentType]]:
        for agent, coordinates in self.positions.items():
            for coord in coordinates:
                self.shadow_board[coord.x][coord.y] = agent
        return self.shadow_board

    def __getitem__(self, item: Coordinate) -> AgentType:
        return self.shadow_board[item.x][item.y]

    @classmethod
    def random(cls, random_seed: Optional[int] = None):
        if random_seed is not None:
            random.seed(random_seed)

        board_size = DEFAULT_BOARD_SIZE
        starting_color = random.choice([AgentType.BLUE, AgentType.RED])
        num_agents_per_type = {
            AgentType.RED: 9 if starting_color == AgentType.RED else 8,
            AgentType.BLUE: 9 if starting_color == AgentType.BLUE else 8,
            AgentType.BLACK: 1,
            AgentType.INNOCENT: (board_size**2) - (8 + 9 + 1),
        }
        chosen_positions = {}
        all_configurations = list(
            itertools.product(*itertools.repeat(range(board_size), 2))
        )
        random.shuffle(all_configurations)

        for agent_type, num_agents in num_agents_per_type.items():
            chosen_positions[agent_type] = all_configurations[:num_agents]
            all_configurations = all_configurations[num_agents:]

        return cls(positions=chosen_positions, starting_color=starting_color)


class Board:
    cards: list[list[str]]
    discovered_agents: list[Coordinate]
    agent_placements: AgentPlacements

    def __init__(
        self,
        words: list[list[str]],
        agent_placements: AgentPlacements,
        discovered_agents: list[Coordinate] = [],
    ):
        super().__init__()

        if any(len(row) != len(words) for row in words):
            raise ValueError("The words array must be a square array.")

        self.words = deepcopy(words)
        self.discovered_agents = discovered_agents[:]
        self.agent_placements = agent_placements.model_copy()
