# File: app/main.py
from fastapi import FastAPI

from app.api.routes import game_router

app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI App!"}

# Mount the router to the FastAPI app
app.include_router(game_router)