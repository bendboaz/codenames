from abc import ABC, abstractmethod

from app.bll.game import Game


class BaseDataAccess(ABC):
    """
    An abstract base class that defines the interface for data access
    in the Codenames codebase.
    Includes methods for retrieving, saving, and manipulating game data
    and utility functions like loading words and agent positions.
    """

    @abstractmethod
    def get_game_by_id(self, game_id: str) -> Game:
        """
        Retrieve a game by its unique ID.

        :param game_id: The unique identifier of the game.
        :return: The game state or None if not found.
        """
        pass

    @abstractmethod
    def save_game(self, game_id: str, game_state: Game):
        """
        Save a game and its current state to the storage.

        :param game_id: The unique identifier of the game.
        :param game_state: The current state of the game.
        """
        pass

    @abstractmethod
    def delete_game(self, game_id: str):
        """
        Delete a game by its unique ID.

        :param game_id: The unique identifier of the game.
        """
        pass

    @abstractmethod
    def load_card_words(self) -> list[str]:
        """
        Load a list of words that can appear on the cards.

        :return: A list of card words.
        """
        pass

    @abstractmethod
    def load_clue_words(self) -> list[str]:
        """
        Load a list of words that can be used as clues during the game.

        :return: A list of clue words.
        """
        pass
