from pydantic import BaseModel


# Pydantic model for the game state
class GameState(BaseModel):
    board: str
    status: str
