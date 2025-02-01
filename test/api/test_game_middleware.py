import pytest
from unittest.mock import MagicMock, patch
from fastapi import FastAPI, Depends
from fastapi.testclient import TestClient
from app.api.dependencies.game_storage import get_or_create_game
from app.dal.local_dal import LocalDataAccess
from app.bll.game import Game


@pytest.fixture
def mock_data_access():
    """Mocked LocalDataAccess instance."""
    return MagicMock(LocalDataAccess)


@pytest.fixture
def mock_game():
    """Returns a mocked game instance."""
    mock_game = MagicMock(Game)
    mock_game.game_id = "test_game_id"
    return mock_game


@pytest.fixture
def app_with_dependency(mock_data_access, mock_game):
    """FastAPI app with `get_or_create_game` dependency."""
    app = FastAPI()

    @app.get("/game/query")
    async def get_game_query(
        game: Game = Depends(get_or_create_game), game_id: str = ""
    ):
        """Fetch game using the `game_id` passed as a query parameter."""
        return {"game_id": game.game_id}

    @app.get("/game/{game_id}")
    async def get_game(game: Game = Depends(get_or_create_game)):
        """Fetch game by ID."""
        return {"game_id": game.game_id}

    @app.post("/game/start")
    async def start_game(game: Game = Depends(get_or_create_game)):
        """Start a new game."""
        return {"game_id": game.game_id}

    @app.post("/game/body")
    async def get_game_body(
        game: Game = Depends(get_or_create_game), request_body: dict = None
    ):
        """Fetch game using the `game_id` provided in the request body."""
        return {"game_id": game.game_id}

    return app


@pytest.fixture
def mock_patched_dependencies(mock_game):
    """Fixture to patch and provide commonly used dependencies.

    This includes:
    - `data_access.get_game_by_id`
    - `data_access.save_game`
    - `Game.new_game`
    """
    with (
        patch(
            "app.api.dependencies.game_storage.data_access.get_game_by_id"
        ) as mock_get_game_by_id,
        patch(
            "app.api.dependencies.game_storage.data_access.save_game"
        ) as mock_save_game,
        patch("app.api.dependencies.game_storage.Game.new_game") as mock_new_game,
    ):
        # Mock behaviors
        mock_get_game_by_id.return_value = mock_game  # Default to returning mock_game
        mock_save_game.return_value = None  # Default to no return for saving
        mock_new_game.return_value = (
            mock_game  # Default to returning mock_game for new_game
        )

        # Yield the mocks
        yield {
            "get_game_by_id": mock_get_game_by_id,
            "save_game": mock_save_game,
            "new_game": mock_new_game,
        }


def test_game_loading_with_dependency(
    mock_patched_dependencies, mock_game, app_with_dependency
):
    """Test loading an existing game using the `get_or_create_game` dependency."""
    # Access the patched `get_game_by_id` mock
    mock_patched_dependencies["get_game_by_id"].return_value = mock_game

    client = TestClient(app_with_dependency)
    response = client.get("/game/test_game_id")  # Test path parameter

    # Assertions
    assert response.status_code == 200
    assert response.json() == {"game_id": "test_game_id"}
    mock_patched_dependencies["get_game_by_id"].assert_called_once_with("test_game_id")


def test_game_loading_from_query(
    mock_patched_dependencies, mock_game, app_with_dependency
):
    """Test that the dependency successfully retrieves game_id from query parameters."""
    client = TestClient(app_with_dependency)
    response = client.get(
        "/game/query?game_id=test_game_id"
    )  # Query parameter test case

    # Assertions
    assert response.status_code == 200
    assert response.json() == {"game_id": "test_game_id"}
    mock_patched_dependencies["get_game_by_id"].assert_called_once_with("test_game_id")


def test_game_loading_from_body(
    mock_patched_dependencies, mock_game, app_with_dependency
):
    """Test that the dependency works when extracting game_id from the request body."""
    client = TestClient(app_with_dependency)
    request_body = {"game_id": "test_game_id"}  # Request body with game_id
    response = client.post("/game/body", json=request_body)  # POST request body test

    # Assertions
    assert response.status_code == 200
    assert response.json() == {"game_id": "test_game_id"}
    mock_patched_dependencies["get_game_by_id"].assert_called_once_with("test_game_id")


def test_game_auto_creation_with_dependency(
    mock_patched_dependencies, mock_game, app_with_dependency
):
    """Test that `get_or_create_game` creates a new game if no `game_id` is provided."""
    mock_patched_dependencies[
        "new_game"
    ].return_value = mock_game  # Ensure new game is mocked
    mock_game.game_id = "new_game_id"

    client = TestClient(app_with_dependency)
    response = client.post("/game/start")  # No game_id provided

    # Assertions
    assert response.status_code == 200
    assert response.json() == {"game_id": "new_game_id"}
    mock_patched_dependencies["new_game"].assert_called_once()
    mock_patched_dependencies["save_game"].assert_called_with("new_game_id", mock_game)


def test_game_not_found_with_dependency(mock_patched_dependencies, app_with_dependency):
    """Test that `get_or_create_game` raises 404 when the game ID is not found."""
    # Simulate "not found" error
    mock_patched_dependencies["get_game_by_id"].side_effect = FileNotFoundError()

    client = TestClient(app_with_dependency)
    response = client.get("/game/nonexistent_id")  # Nonexistent game_id

    # Assertions
    assert response.status_code == 404
    assert response.json() == {"detail": "Game with ID nonexistent_id not found."}
    mock_patched_dependencies["get_game_by_id"].assert_called_once_with(
        "nonexistent_id"
    )


def test_game_saving_after_dependency_execution(
    mock_patched_dependencies, mock_game, app_with_dependency
):
    """Test that the game is saved after endpoint execution."""
    client = TestClient(app_with_dependency)
    response = client.get("/game/test_game_id")  # Retrieve test game

    # Assertions
    assert response.status_code == 200
    assert response.json() == {"game_id": "test_game_id"}
    mock_patched_dependencies["save_game"].assert_called_with("test_game_id", mock_game)
    mock_patched_dependencies["get_game_by_id"].assert_called_once_with("test_game_id")
