import uuid
from typing import TYPE_CHECKING

from pydantic import BaseModel

from app.bll.board import Board
from app.bll.defaults import DEFAULT_BOARD_SIZE
from app.bll.game_utils import change_player
from app.bll.types import (
    GameEndStatus,
    AgentType,
    GameState,
    Clue,
    Coordinate,
    CurrentTurnState,
)

if TYPE_CHECKING:
    from app.dal.base_data_access import BaseDataAccess


class InvalidGuessException(Exception):
    """Exception raised for invalid guesses during the game."""

    pass


class Game(BaseModel):
    game_id: str
    board: Board
    game_end_status: GameEndStatus
    current_turn: CurrentTurnState

    @classmethod
    def new_game(cls, words_provider: "BaseDataAccess"):
        board = Board.random_with_words(
            words_provider.load_card_words()[: DEFAULT_BOARD_SIZE**2]
        )
        return cls(
            game_id=str(uuid.uuid4()),
            board=board,
            game_end_status=GameEndStatus.ONGOING,
            current_turn=CurrentTurnState(team=board.agent_placements.starting_color),
        )

    def get_game_description_for_operative(self) -> GameState:
        """Returns a filtered description of the current game state for operatives.

        This method compiles a limited representation of the game's current state
        that is suitable for operatives. It includes only the information necessary
        for them to make decisions during gameplay.

        :return: A `GameState` object containing the game's unique ID, the list of words
                 on the board, the current player's color, and the victory state of the game.
        """
        game_id = self.game_id
        words = self.board.words
        current_turn = self.current_turn
        victory_state = self.game_end_status
        return GameState(
            game_id=game_id,
            words=words,
            current_turn=current_turn,
            victory_state=victory_state,
        )

    def get_game_description(self, is_spymaster: bool):
        """Gets the appropriate game description based on the user's role.

        This method evaluates whether the user is a spymaster or an operative
        and returns the corresponding description of the game accordingly.
        If the user is a spymaster, the method directly returns the relevant
        game description. If the user is an operative, it invokes the method
        that provides the game description tailored for operatives.

        :param is_spymaster: A boolean indicating if the user is a spymaster.
        :return: The game description customized for the user's role.
        """
        return self if is_spymaster else self.get_game_description_for_operative()

    def make_move(self, guess: Coordinate) -> [AgentType, GameEndStatus, Clue, bool]:
        """Process a move and return the updated game information.

        Make a move in the game based on the given guess. This method processes the player's
        guess by revealing a card on the board, increments the count of guesses made in the
        current turn, and determines if the turn is over. Additionally, it updates the current
        turn state and checks if the game has ended. The outcome of the guess, the game's end
        status, the updated turn state, and a flag indicating if the turn is over are returned.

        :param guess: A coordinate representing the location of the card being guessed on the board.
        :type guess: Coordinate

        :return: A tuple containing the outcome of the guess, the game end status, the updated
                 current turn state, and a boolean indicating if the turn has ended.
        :rtype: tuple[AgentType, GameEndStatus, Clue, bool]
        """
        try:
            guess_outcome = self.board.reveal_card(guess)
        except ValueError as e:
            raise InvalidGuessException(str(e)) from e

        self.current_turn.guesses_made += 1
        is_turn_over = (guess_outcome != self.current_turn.team) or (
            self.current_turn.guesses_made == self.current_turn.clue.num_guesses + 1
        )
        if is_turn_over:
            new_turn = CurrentTurnState(team=change_player(self.current_turn.team))
            self.current_turn = new_turn

        game_end_status = self.board.check_game_end()

        return (
            guess_outcome,
            game_end_status,
            self.current_turn,
            is_turn_over,
        )
