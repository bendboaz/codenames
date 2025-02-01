from abc import ABC, abstractmethod

from app.bll.types import Clue, Coordinate, TeamColor


class Player:
    """
    Base class for game players (Spymasters and Operatives).
    """

    @abstractmethod
    def team(self) -> TeamColor:
        pass


class Spymaster(Player, ABC):
    """
    Represents a Spymaster player who provides clues.
    """

    @abstractmethod
    def offer_clue(self, board: dict) -> Clue:
        """
        Offers a clue to the Operative(s) based on the current board state.
        :param board: A dictionary representing the filtered board, containing words and discovered agents.
        :return: An instance of the Clue class.
        """
        pass


class Operative(Player, ABC):
    """
    Represents an Operative player who guesses words based on clues.
    """

    @abstractmethod
    def guess_word(self, clue: Clue) -> Coordinate | None:
        """
        Guess a word on the board based on the given clue.
        :param clue: The clue provided by the Spymaster to guide the guess.
        :return: The coordinate of the guessed word or None if no guess is made.
        """
        pass
