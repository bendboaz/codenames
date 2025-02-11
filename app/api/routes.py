from fastapi import APIRouter, HTTPException, Depends, Body
from typing import Dict, Any

from app.api.dependencies.game_storage import get_or_create_game
from app.bll.game import Game
from app.bll.types import Clue

game_router = APIRouter(prefix="/game", tags=["game"])


@game_router.post("/start")
async def start_new_game(game: Game = Depends(get_or_create_game)):
    """
    Start a new game by creating and initializing the board.
    """
    # Initialize an empty game board for demonstration purposes
    return {"game_id": game.game_id}


@game_router.get("/{game_id}/board")
async def get_board(game: Game = Depends(get_or_create_game)):
    """
    Retrieve the state of the board for the given game.
    """
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")

    return {"game_id": game.game_id, "board": game.board}


@game_router.post("/{game_id}/offer-clue")
async def handle_clue(
    game: Game = Depends(get_or_create_game), clue: Dict[str, Any] = Body()
):
    """
    Submit a clue or guess for the game.
    """
    game.set_clue(Clue(**clue))
    return {"game_id": game.game_id, "clue": clue}


@game_router.post("/{game_id}/guess")
async def play_move(
    game: Game = Depends(get_or_create_game), move: Dict[str, Any] = Body()
):
    """
    Submit a clue or guess for the game.
    """
    move_outcome = game.make_move(move["guess"])
    return {"game_id": game.game_id, "move": move, "outcome": move_outcome}


@game_router.get("/{game_id}")
async def get_game_status(game: Game = Depends(get_or_create_game)):
    """
    Get the current game status, including progress and scores.
    """

    return {
        "game_id": game.game_id,
        "victory_status": game.game_end_status,
        "current_turn": game.current_turn,
    }
