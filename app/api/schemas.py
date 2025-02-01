from pydantic import BaseModel


# Pydantic model for the game state
class OldGameState(BaseModel):
    board: str
    status: str
