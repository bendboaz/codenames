from pathlib import Path

from app.bll.game import Game
from app.dal.base_data_access import BaseDataAccess


class LocalDataAccess(BaseDataAccess):
    def __init__(self, root_dir: Path):
        if not root_dir.exists():
            raise ValueError(f"Path {str(root_dir)} does not exist!")

        self.root_dir = root_dir

    def get_game_by_id(self, game_id: int) -> Game:
        game_file = self.root_dir / "games" / f"{game_id}.json"
        if not game_file.exists():
            raise FileNotFoundError(f"Game with ID {game_id} does not exist.")

        with game_file.open("r") as f:
            return Game.model_validate_json(f.read())

    def save_game(self, game_id: int, game_state: Game):
        games_dir = self.root_dir / "games"
        games_dir.mkdir(parents=True, exist_ok=True)

        game_file = games_dir / f"{game_id}.json"
        with game_file.open("w") as f:
            f.write(game_state.model_dump_json())

    def delete_game(self, game_id: int):
        game_file = self.root_dir / "games" / f"{game_id}.json"
        if game_file.exists():
            game_file.unlink()
        else:
            raise FileNotFoundError(f"Game with ID {game_id} does not exist.")

    def load_card_words(self) -> list[str]:
        card_words_file = self.root_dir / "card_words.txt"
        if not card_words_file.exists():
            raise FileNotFoundError("Card words file does not exist.")

        with card_words_file.open("r") as f:
            return [line.strip() for line in f.readlines()]

    def load_clue_words(self) -> list[str]:
        clue_words_file = self.root_dir / "clue_words.txt"
        if not clue_words_file.exists():
            raise FileNotFoundError("Clue words file does not exist.")

        with clue_words_file.open("r") as f:
            return [line.strip() for line in f.readlines()]
