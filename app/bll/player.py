from abc import ABC, abstractmethod

from app.bll.game import Game
from app.bll.types import Clue, Coordinate, TeamColor, GameState, AgentType


class Player:
    """
    Base class for game players (Spymasters and Operatives).
    """

    def __init__(self, team: TeamColor):
        if team not in (AgentType.RED, AgentType.BLUE):
            raise ValueError(f"team must be an instance of {TeamColor}, got {team}")

        self.team = team


class Spymaster(Player, ABC):
    """
    Represents a Spymaster player who provides clues.
    """

    @abstractmethod
    def prefix_turn(self, game: Game):
        pass

    @abstractmethod
    def offer_clue(self) -> Clue:
        """Offers a clue to the Operative(s) based on the current board state.
        :return: An instance of the Clue class.
        """
        pass


class Operative(Player, ABC):
    """
    Represents an Operative player who guesses words based on clues.
    """

    @abstractmethod
    def prefix_turn(self, game: GameState):
        pass

    @abstractmethod
    def guess_word(self, game: GameState) -> Coordinate | None:
        """Guess a word on the board based on the given clue.

        :param game: The current state of the game visible to the Operative, including the board,
                     available words, and game progress.
        :return: The coordinate of the guessed word or None if no guess is made.
        """
        pass
