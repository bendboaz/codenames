import uuid

import pytest
from unittest.mock import create_autospec, patch, MagicMock

from app.bll.defaults import DEFAULT_BOARD_SIZE
from app.bll.game import Game, InvalidGuessException, CurrentTurnState
from app.bll.board import Board
from app.bll.types import AgentType, Coordinate, Clue, GameEndStatus
from test.utils import get_test_board


def test_get_game_description_for_operative():
    # Mock the game's board and create an instance of Game
    board = get_test_board()
    game = Game(
        board=board,
        game_id="1234",
        status="running",
        game_end_status=GameEndStatus.ONGOING,
        current_turn=CurrentTurnState(team=AgentType.RED),
    )

    # Call the method to test game description for operative
    result = game.get_game_description_for_operative()

    # Assertions
    assert result.game_id == "1234"
    assert result.words == board.words
    assert result.current_turn.team == AgentType.RED
    assert result.victory_state == GameEndStatus.ONGOING


def test_get_game_description():
    with patch(
        "app.bll.game.Game.get_game_description_for_operative",
        return_value="mocked_value",
    ) as mock_method:
        # Mock the game's board and create an instance of Game
        board = get_test_board()
        game = Game(
            board=board,
            game_id="game123",
            game_end_status=GameEndStatus.ONGOING,
            current_turn=CurrentTurnState(team=AgentType.RED),
        )

        # Test for spymaster description (should return the full game object)
        spymaster_result = game.get_game_description(is_spymaster=True)
        assert spymaster_result == game  # Spymaster receives a full game instance

        # Test for operative description
        game.get_game_description(is_spymaster=False)
        mock_method.assert_called_once()  # Verify method call


def test_make_move_valid():
    # Mock the game's board
    dummy_board = get_test_board()

    mock_board = create_autospec(Board, instance=True)
    mock_board.words = dummy_board.words
    mock_board.reveal_card.return_value = AgentType.RED
    mock_board.check_game_end.return_value = GameEndStatus.ONGOING

    # Create a Clue and CurrentTurnState for the game
    clue = Clue(clue="keyword", num_guesses=2)
    turn_state = CurrentTurnState(team=AgentType.RED, clue=clue)

    # Instantiate a Game object
    game = Game(
        board=mock_board,
        game_id="game123",
        status=None,
        game_end_status=GameEndStatus.ONGOING,
        current_turn=turn_state,
    )

    # Perform a valid move
    guess = Coordinate(x=0, y=1)
    result = game.make_move(guess)

    # Assertions
    assert result[0] == AgentType.RED  # Guess outcome matches current player
    assert result[1] == GameEndStatus.ONGOING  # Game continues
    assert result[2].guesses_made == 1  # Increment guess count
    assert result[3] is False  # Turn is not over


def test_make_move_turn_over():
    # Mock the game's board and create a turn-over scenario
    dummy_board = get_test_board()

    mock_board = create_autospec(Board, instance=True)
    mock_board.words = dummy_board.words
    mock_board.reveal_card.return_value = AgentType.BLUE
    mock_board.check_game_end.return_value = GameEndStatus.ONGOING

    # Create a Clue and CurrentTurnState for the game
    clue = Clue(clue="turnover", num_guesses=1)
    turn_state = CurrentTurnState(team=AgentType.RED, clue=clue, guesses_made=1)

    # Instantiate Game object
    game = Game(
        board=mock_board,
        game_id="game123",
        status=None,
        game_end_status=GameEndStatus.ONGOING,
        current_turn=turn_state,
    )

    # Perform a move that ends the turn
    guess = Coordinate(x=1, y=1)
    result = game.make_move(guess)

    # Assertions
    assert result[0] == AgentType.BLUE  # Guess outcome
    assert result[1] == GameEndStatus.ONGOING  # Game is still ongoing
    assert result[2].team == AgentType.BLUE  # TeamColor switched to BLUE
    assert result[2].guesses_made == 0  # Next turn starts with 0 guesses
    assert result[3] is True  # Turn is over


def test_make_move_game_over():
    # Mock the board to simulate game over scenario
    dummy_board = get_test_board()

    mock_board = create_autospec(Board, instance=True)
    mock_board.words = dummy_board.words
    mock_board.reveal_card.return_value = AgentType.RED
    mock_board.check_game_end.return_value = GameEndStatus.RED_VICTORY

    # Create game state for a single valid turn
    clue = Clue(clue="victory", num_guesses=1)
    turn_state = CurrentTurnState(team=AgentType.RED, clue=clue, guesses_made=0)
    game = Game(
        board=mock_board,
        game_id="game123",
        status=None,
        game_end_status=GameEndStatus.ONGOING,
        current_turn=turn_state,
    )

    # Perform a game-ending move
    guess = Coordinate(x=2, y=2)
    result = game.make_move(guess)

    # Assertions
    assert result[1] == GameEndStatus.RED_VICTORY  # Game ends with RED victory


def test_make_move_invalid_guess():
    # Mock the board to raise a ValueError for invalid guesses
    dummy_board = get_test_board()

    mock_board = create_autospec(Board, instance=True)
    mock_board.words = dummy_board.words
    mock_board.reveal_card.side_effect = ValueError("Invalid guess!")
    mock_board.check_game_end.return_value = GameEndStatus.ONGOING

    # Create game with a basic turn state
    turn_state = CurrentTurnState(team=AgentType.RED)
    game = Game(
        board=mock_board,
        game_id="game123",
        status=None,
        game_end_status=GameEndStatus.ONGOING,
        current_turn=turn_state,
    )

    # Perform an invalid move and expect an exception
    guess = Coordinate(x=1, y=1)
    with pytest.raises(InvalidGuessException, match="Invalid guess!"):
        game.make_move(guess)


def test_game_new_game():
    # Mock a words provider
    words_provider = MagicMock()
    words_provider.load_card_words.return_value = [
        f"word{i}" for i in range(DEFAULT_BOARD_SIZE**2)
    ]

    # Call Game.new_game
    game = Game.new_game(words_provider)

    # Assertions
    assert isinstance(game, Game)  # Ensure a Game instance is returned
    assert isinstance(game.board, Board)  # Ensure the board is a Board instance
    assert len(game.board.words) == DEFAULT_BOARD_SIZE  # Ensure the board size matches
    assert all(
        len(row) == DEFAULT_BOARD_SIZE for row in game.board.words
    )  # Ensure the board is square

    # Validate the game_id is a UUID string
    uuid_obj = uuid.UUID(
        game.game_id, version=4
    )  # This will raise ValueError if not a valid UUID
    assert str(uuid_obj) == game.game_id

    # Ensure the game is in the ONGOING state
    assert game.game_end_status == GameEndStatus.ONGOING

    # Check that words_provider was used correctly
    words_provider.load_card_words.assert_called()  # Ensure it was called at least once
