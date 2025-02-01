import io

import pytest
from unittest.mock import MagicMock, patch
from app.bll.human_players import HumanSpymaster, HumanOperative
from app.bll.types import Clue, Coordinate, Card, GameState, AgentType


@pytest.fixture
def mocked_game():
    # Create a mock game object with the necessary attributes
    mocked_game = MagicMock()
    mocked_game.board.words = [
        [
            Card(word="word1", card_type=AgentType.UNKNOWN),
            Card(word="word2", card_type=AgentType.UNKNOWN),
        ],
        [
            Card(word="word3", card_type=AgentType.UNKNOWN),
            Card(word="word4", card_type=AgentType.UNKNOWN),
        ],
    ]
    mocked_game.board.agent_placements.positions = {
        AgentType.RED: [
            Coordinate.from_tuple(0, 0),
            Coordinate.from_tuple(1, 1),
        ],
        AgentType.BLUE: [Coordinate.from_tuple(0, 1), Coordinate.from_tuple(1, 0)],
    }
    mocked_game.board.discovered_agents = [
        Coordinate.from_tuple(0, 0)
    ]  # One word has been revealed
    return mocked_game


@pytest.fixture
def mocked_game_state():
    # Create a mock game state object
    mocked_game_state = MagicMock(spec=GameState)
    mocked_game_state.words = [
        [
            Card(word="word1", card_type=AgentType.UNKNOWN),
            Card(word="word2", card_type=AgentType.UNKNOWN),
        ],
        [
            Card(word="word3", card_type=AgentType.UNKNOWN),
            Card(word="word4", card_type=AgentType.UNKNOWN),
        ],
    ]
    mocked_game_state.current_turn = MagicMock()
    mocked_game_state.current_turn.clue = Clue(clue="test-clue", num_guesses=2)
    mocked_game_state.current_turn.guesses_made = 1
    return mocked_game_state


### HumanSpymaster Tests ###


def test_human_spymaster_offer_clue():
    spymaster = HumanSpymaster(AgentType.RED)

    # Mock user input for a clue and number
    with patch("builtins.input", side_effect=["clue-word", "3"]):
        clue = spymaster.offer_clue()

        # Verify Clue object is created correctly
        assert clue.clue == "clue-word"
        assert clue.num_guesses == 3


### HumanOperative Tests ###


@patch("sys.stdout", new_callable=io.StringIO)
def test_human_operative_prefix_turn(mock_out, mocked_game_state):
    operative = HumanOperative(AgentType.BLUE)
    operative.prefix_turn(mocked_game_state)

    # Verify output includes the correct prompt for the operative
    output = mock_out.getvalue()
    assert "Blue operative, it is your turn!" in output


def test_human_operative_guess_word_valid(mocked_game_state):
    operative = HumanOperative(AgentType.BLUE)

    # Mock input for a valid guess
    with patch("builtins.input", return_value="1,0"):
        guess = operative.guess_word(mocked_game_state)

        # Verify the returned Coordinate object is correct
        assert guess == Coordinate.from_tuple(1, 0)


@patch("sys.stdout", new_callable=io.StringIO)
def test_human_operative_guess_word_forfeit(mock_out, mocked_game_state):
    operative = HumanOperative(AgentType.BLUE)

    # Mock input for forfeiting the turn
    with patch("builtins.input", return_value="forfeit"):
        guess = operative.guess_word(mocked_game_state)

        # Verify None is returned
        assert guess is None

        # Verify the forfeit message is displayed
        output = mock_out.getvalue()
        assert "You have chosen to forfeit the rest of your turn." in output


@patch("sys.stdout", new_callable=io.StringIO)
def test_human_operative_guess_word_invalid(mock_out, mocked_game_state):
    operative = HumanOperative(AgentType.BLUE)

    # Mock invalid input followed by forfeit
    with patch("builtins.input", side_effect=["invalid", "forfeit"]):
        guess = operative.guess_word(mocked_game_state)

        # Verify None is returned after forfeiting
        assert guess is None

        # Verify the invalid input message is displayed
        output = mock_out.getvalue()
        assert "Invalid input. Please enter coordinates" in output
        assert "You have chosen to forfeit the rest of your turn." in output
