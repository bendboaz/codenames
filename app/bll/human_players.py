from app.api.display_utils import show_words
from app.bll.game import Game
from app.bll.player import Spymaster, Operative
from app.bll.types import Clue, Coordinate, TeamColor, GameState


class HumanSpymaster(Spymaster):
    def __init__(self, team: TeamColor):
        super().__init__(team)

        self.current_turn = {}

    def prefix_turn(self, game: Game):
        self.current_turn["game"] = game
        print("Current Board:")
        show_words(game.board.words)

        print(f"{self.team.value.capitalize()} spymaster, it is your turn!")
        choice = (
            input(
                "Do you want to see your team's remaining words before guessing? (yes/no): "
            )
            .strip()
            .lower()
        )
        if choice == "yes":
            print("Your team's remaining words:")
            for word in game.board.agent_placements.positions[self.team]:
                if word in game.board.discovered_agents:
                    continue
                print(
                    f"Word: {game.board.words[word.x][word.y].word}, Coordinates: {word}"
                )

    def offer_clue(self) -> Clue:
        clue = input("Enter your clue: ")
        num = int(input("Enter the number of cards related to the clue: "))
        return Clue(clue=clue, num_guesses=num)


class HumanOperative(Operative):
    def __init__(self, team: TeamColor):
        super().__init__(team)

        self.current_turn = {}

    def prefix_turn(self, game: GameState):
        self.current_turn["game"] = game
        print(f"{self.team.value.capitalize()} operative, it is your turn!")

    def guess_word(self, game: GameState) -> Coordinate | None:
        self.current_turn["game"] = game

        show_words(game.words)
        print(f'Your clue is: "{game.current_turn.clue.clue}".')
        print(
            f"You have so far guessed {game.current_turn.guesses_made} out of {game.current_turn.clue.num_guesses} words connected to that clue."
        )

        while True:
            guess = (
                input(
                    'Enter your guess (format: x,y or type "forfeit" to end your turn): '
                )
                .strip()
                .lower()
            )
            if guess == "forfeit":
                print("You have chosen to forfeit the rest of your turn.")
                return None
            try:
                x, y = map(int, guess.split(","))
                return Coordinate(x=x, y=y)
            except ValueError:
                print(
                    'Invalid input. Please enter coordinates in the format x,y or type "forfeit" to end your turn.'
                )
