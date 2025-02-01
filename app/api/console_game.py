from app.bll.game import Game
from app.bll.game_utils import change_player
from app.bll.human_players import HumanSpymaster, HumanOperative
from app.bll.types import AgentType, GameEndStatus, TeamColor
from app.dal.local_dal import LocalDataAccess


class ConsoleCodenames:
    def __init__(self):
        self.game = None
        self.players = None
        self.dal = LocalDataAccess("data")

    def run_new_game(self):
        self.game = Game.new_game(self.dal)

        self.players = {
            AgentType.RED: (
                HumanSpymaster(AgentType.RED),
                HumanOperative(AgentType.RED),
            ),
            AgentType.BLUE: (
                HumanSpymaster(AgentType.BLUE),
                HumanOperative(AgentType.BLUE),
            ),
        }

        self.run_game()

    def run_game(self):
        game_end = False
        winner: TeamColor | None = None
        current_player = self.game.board.agent_placements.starting_color
        while not game_end:
            spymaster, operative = self.players[current_player]

            spymaster.prefix_turn(self.game.get_game_description(is_spymaster=True))
            self.game.set_clue(spymaster.offer_clue())

            operative.prefix_turn(self.game.get_game_description(is_spymaster=False))
            should_turn_end = False
            while not should_turn_end and not game_end:
                (
                    guess_outcome,
                    game_end_status,
                    current_turn_state,
                    should_turn_end,
                ) = self.game.make_move(
                    operative.guess_word(
                        self.game.get_game_description(is_spymaster=False)
                    )
                )

                if game_end_status != GameEndStatus.ONGOING:
                    game_end = True
                    winner_map = {
                        GameEndStatus.BLACK_REVEALED: change_player(current_player),
                        GameEndStatus.RED_VICTORY: AgentType.RED,
                        GameEndStatus.BLUE_VICTORY: AgentType.BLUE,
                    }
                    winner = winner_map[game_end_status]

            current_player = change_player(current_player)
        print(f"Winner is: {winner}! Congratulations!")


if __name__ == "__main__":
    game_runner = ConsoleCodenames()
    game_runner.run_new_game()
