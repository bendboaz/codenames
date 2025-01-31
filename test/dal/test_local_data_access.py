import re

import pytest
from pathlib import Path
from unittest.mock import patch

from app.dal.local_dal import LocalDataAccess
from app.bll.game import Game
from app.bll.types import Card, AgentType, Coordinate, GameStatus, GameEndStatus
from app.bll.board import Board, AgentPlacements


@pytest.fixture
def temp_dir(tmp_path):
    """Fixture for creating a temporary directory."""
    return tmp_path


def create_mock_board():
    # Mock data for words and agent placements
    words = [
        [
            Card(word="word1", card_type=AgentType.UNKNOWN),
            Card(word="word2", card_type=AgentType.UNKNOWN),
        ],
        [
            Card(word="word3", card_type=AgentType.UNKNOWN),
            Card(word="word4", card_type=AgentType.UNKNOWN),
        ],
    ]

    agent_positions = {
        AgentType.RED: [Coordinate(x=0, y=0), Coordinate(x=1, y=0)],
        AgentType.BLUE: [Coordinate(x=0, y=1), Coordinate(x=1, y=1)],
        AgentType.BLACK: [],
        AgentType.INNOCENT: [],
    }

    agent_placements = AgentPlacements(
        positions=agent_positions, starting_color=AgentType.RED
    )

    return Board(words=words, agent_placements=agent_placements)


def test_initializer_valid_path(temp_dir):
    """Test initialization of LocalDataAccess with a valid path."""
    local_dal = LocalDataAccess(root_dir=temp_dir)
    assert local_dal.root_dir == temp_dir


def test_initializer_invalid_path():
    """Test initialization of LocalDataAccess with an invalid path."""
    invalid_path = Path("non/existent/path")
    with pytest.raises(
        ValueError, match=re.escape(f"Path {str(invalid_path)} does not exist!")
    ):
        LocalDataAccess(root_dir=invalid_path)


def test_get_game_by_id_file_not_found(temp_dir):
    """Test get_game_by_id when the game file does not exist."""
    local_dal = LocalDataAccess(root_dir=temp_dir)
    with pytest.raises(FileNotFoundError, match="Game with ID 1 does not exist."):
        local_dal.get_game_by_id(game_id=1)


def test_get_game_by_id_valid(temp_dir):
    """Test get_game_by_id when the game file exists."""
    game_id = 1
    game_data = '{"game_id": "1", "status": "ONGOING", "current_turn": {"player": "RED", "clue": null, "guesses_made": 0}}'
    temp_dir_games = temp_dir / "games"
    temp_dir_games.mkdir()
    game_file = temp_dir_games / f"{game_id}.json"
    game_file.write_text(game_data)

    with patch("app.bll.game.Game.model_validate_json") as mock_validate:
        mock_validate.return_value = (
            "Game Object"  # Replace with a valid mock Game object if needed
        )
        local_dal = LocalDataAccess(root_dir=temp_dir)
        result = local_dal.get_game_by_id(game_id=game_id)
        mock_validate.assert_called_once_with(game_data)
        assert result == "Game Object"


def test_save_game_valid(temp_dir):
    """Test saving a game to the file system."""
    temp_dir_games = temp_dir / "games"
    local_dal = LocalDataAccess(root_dir=temp_dir)

    game_id = 1
    mock_board = create_mock_board()

    # Updated to match the new Game signature
    game_state = Game(
        game_id="1",  # Matches the `game_id` field in the `Game` class
        board=mock_board,
        status=GameStatus.INITIALIZED,
        game_end_status=GameEndStatus.ONGOING,
        current_turn={"player": AgentType.RED, "clue": None, "guesses_made": 0},
    )

    # Mock the `model_dump_json` method of the `Game` object (used in `save_game`)
    with patch("app.bll.game.Game.model_dump_json", return_value="Game Data JSON"):
        local_dal.save_game(game_id=game_id, game_state=game_state)

    saved_file = temp_dir_games / f"{game_id}.json"
    assert saved_file.exists()
    assert saved_file.read_text() == "Game Data JSON"


def test_delete_game_existing_file(temp_dir):
    """Test deleting an existing game file."""
    game_id = 1
    temp_dir_games = temp_dir / "games"
    temp_dir_games.mkdir()
    game_file = temp_dir_games / f"{game_id}.json"
    game_file.touch()  # Create an empty file

    local_dal = LocalDataAccess(root_dir=temp_dir)
    local_dal.delete_game(game_id=game_id)

    assert not game_file.exists()


def test_delete_game_missing_file(temp_dir):
    """Test deleting a non-existent game file."""
    game_id = 1
    local_dal = LocalDataAccess(root_dir=temp_dir)
    with pytest.raises(
        FileNotFoundError, match=f"Game with ID {game_id} does not exist."
    ):
        local_dal.delete_game(game_id=game_id)


def test_load_card_words_file_not_found(temp_dir):
    """Test loading card words when the file does not exist."""
    local_dal = LocalDataAccess(root_dir=temp_dir)
    with pytest.raises(FileNotFoundError, match="Card words file does not exist."):
        local_dal.load_card_words()


def test_load_card_words_valid(temp_dir):
    """Test loading card words when the file exists."""
    card_words = ["word1", "word2", "word3"]
    card_words_file = temp_dir / "card_words.txt"
    card_words_file.write_text("\n".join(card_words))

    local_dal = LocalDataAccess(root_dir=temp_dir)
    result = local_dal.load_card_words()

    assert result == card_words


def test_load_clue_words_file_not_found(temp_dir):
    """Test loading clue words when the file does not exist."""
    local_dal = LocalDataAccess(root_dir=temp_dir)
    with pytest.raises(FileNotFoundError, match="Clue words file does not exist."):
        local_dal.load_clue_words()


def test_load_clue_words_valid(temp_dir):
    """Test loading clue words when the file exists."""
    clue_words = ["clue1", "clue2", "clue3"]
    clue_words_file = temp_dir / "clue_words.txt"
    clue_words_file.write_text("\n".join(clue_words))

    local_dal = LocalDataAccess(root_dir=temp_dir)
    result = local_dal.load_clue_words()

    assert result == clue_words
