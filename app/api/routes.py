from fastapi import FastAPI, APIRouter, HTTPException
from typing import Dict, Any

from app.api.schemas import GameState

game_router = APIRouter(prefix="/game", tags=["game"])



# Dictionary to hold mock game data for demonstration
games: Dict[int, GameState] = {}
game_id_counter = 1


@game_router.post("/start")
async def start_new_game():
    """
    Start a new game by creating and initializing the board.
    """
    global game_id_counter
    game_id = game_id_counter
    game_id_counter += 1

    # Initialize an empty game board for demonstration purposes
    games[game_id] = GameState(board="Initialized", status="in_progress")
    return {"game_id": game_id, "message": "Game started!"}


@game_router.get("/{game_id}/board")
async def get_board(game_id: int):
    """
    Retrieve the state of the board for the given game.
    """
    game = games.get(game_id)
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")

    return {"game_id": game_id, "board": game.board}


@game_router.post("/{game_id}/play")
async def play_move(game_id: int, move: Dict[str, Any]):
    """
    Submit a clue or guess for the game.
    """
    game = games.get(game_id)
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")

    # TODO: Implement move validation and processing here
    return {"game_id": game_id, "move": move, "message": "Move processed!"}


@game_router.get("/{game_id}")
async def get_game_status(game_id: int):
    """
    Get the current game status, including progress and scores.
    """
    game = games.get(game_id)
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")

    return {"game_id": game_id, "status": game.status}
