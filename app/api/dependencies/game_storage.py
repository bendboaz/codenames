from pathlib import Path

from fastapi import HTTPException, Request

from app.bll.game import Game
from app.dal.local_dal import LocalDataAccess

data_access = LocalDataAccess(Path("data"))  # Initialize once globally


async def get_or_create_game(game_id: str | None = None, request: Request = None):
    """
    Dependency to load a game by ID or create a new game if no `game_id` is provided.
    """
    # Path parameters take precedence (already passed in `game_id` argument)
    if not game_id:
        # Try to extract `game_id` from query parameters
        game_id = request.query_params.get("game_id")

    if not game_id and request.method in {"POST", "PUT"}:
        # Attempt to extract `game_id` from the body (only for POST/PUT requests)
        try:
            body = await request.json()
            game_id = body.get("game_id")
        except ValueError:
            # No game_id found, proceed and create a new one later.
            pass

    if game_id:
        # Load game by ID
        try:
            game = data_access.get_game_by_id(game_id)
        except FileNotFoundError:
            raise HTTPException(
                status_code=404, detail=f"Game with ID {game_id} not found."
            )
    else:
        # If game_id isn't present, create a new game
        game = Game.new_game(data_access)
        data_access.save_game(game.game_id, game)

    yield game

    # Auto-save the game after endpoint execution
    data_access.save_game(game.game_id, game)
