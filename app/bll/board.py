import itertools
import random
from copy import deepcopy
from typing import Optional

from pydantic import BaseModel, Field

from app.bll.defaults import DEFAULT_BOARD_SIZE
from app.bll.game_utils import get_empty_board
from app.bll.types import AgentType, Coordinate, GameEndStatus, Card


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
        all_coordinates = list(
            itertools.product(*itertools.repeat(range(board_size), 2))
        )
        all_coordinates = [Coordinate.from_tuple(*coor) for coor in all_coordinates]
        random.shuffle(all_coordinates)

        for agent_type, num_agents in num_agents_per_type.items():
            chosen_positions[agent_type] = all_coordinates[:num_agents]
            all_coordinates = all_coordinates[num_agents:]

        return cls(positions=chosen_positions, starting_color=starting_color)


class Board(BaseModel):
    words: list[list[Card]]
    discovered_agents: list[Coordinate]
    agent_placements: AgentPlacements

    def __init__(
        self,
        words: list[list[Card]],
        agent_placements: AgentPlacements,
        discovered_agents: list[Coordinate] = [],
    ):
        if len(words) == 0 or any(len(row) != len(words) for row in words):
            raise ValueError("The words array must be a square array.")

        super().__init__(
            words=deepcopy(words),
            agent_placements=agent_placements.model_copy(),
            discovered_agents=discovered_agents[:],
        )

    @classmethod
    def from_words_and_placements(
        cls, words: list[list[str]], placements: AgentPlacements
    ):
        words = [
            [Card(word=word, card_type=AgentType.UNKNOWN) for word in row]
            for row in words
        ]
        return cls(words, placements)

    @classmethod
    def random_with_words(cls, words: list[str], random_seed: Optional[int] = None):
        if random_seed is not None:
            random.seed(random_seed)

        board_size = DEFAULT_BOARD_SIZE
        if len(words) != board_size**2:
            raise ValueError(f"The number of words must be exactly {board_size**2}.")

        random.shuffle(words)
        formatted_words = [
            [
                Card(word=word, card_type=AgentType.UNKNOWN)
                for word in words[i : i + board_size]
            ]
            for i in range(0, len(words), board_size)
        ]

        agent_placements = AgentPlacements.random(random_seed=random_seed)
        return cls(words=formatted_words, agent_placements=agent_placements)

    def reveal_card(self, coordinate: Coordinate) -> AgentType:
        # Ensure the guessed coordinate is within the bounds of the board
        if not (
            0 <= coordinate.x < len(self.words)
            and 0 <= coordinate.y < len(self.words[0])
        ):
            raise ValueError("The guessed coordinate is out of bounds.")

        # Ensure the guessed coordinate has not already been revealed
        if self.words[coordinate.x][coordinate.y].card_type != AgentType.UNKNOWN:
            raise ValueError("This coordinate has already been revealed.")

        agent_type = self.agent_placements[coordinate]
        self.words[coordinate.x][coordinate.y].card_type = agent_type
        self.discovered_agents.append(coordinate)
        return agent_type

    def check_game_end(self) -> GameEndStatus:
        """
        Check if the game has ended and return the result as a GameEndStatus.
        Possible outcomes are: RED_VICTORY, BLUE_VICTORY, BLACK_REVEALED, or ONGOING if the game is still ongoing.
        """
        red_agents_remaining = len(
            [
                coord
                for coord in self.agent_placements.positions[AgentType.RED]
                if coord not in self.discovered_agents
            ]
        )
        blue_agents_remaining = len(
            [
                coord
                for coord in self.agent_placements.positions[AgentType.BLUE]
                if coord not in self.discovered_agents
            ]
        )

        # Check if all RED or all BLUE agents have been revealed
        if red_agents_remaining == 0:
            return GameEndStatus.RED_VICTORY
        if blue_agents_remaining == 0:
            return GameEndStatus.BLUE_VICTORY

        # Check if the black card has been revealed
        for coord in self.discovered_agents:
            if self.agent_placements[coord] == AgentType.BLACK:
                return GameEndStatus.BLACK_REVEALED

        return GameEndStatus.ONGOING
