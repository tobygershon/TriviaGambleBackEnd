import random as r
class GameBoard:

    def __init__(self):
        self.games_dict = {}
        self.current_games_id_set = set()

    # checks if randomly generated game ID already exists in the current games set.  adds new unique game ID to set and dict
    def add_new_game_to_set_and_dict(self, game):
        while game.game_id in self.current_games_id_set:
            game.game_id = r.randint(10000, 999999)

        self.current_games_id_set.add(game.game_id)
        self.games_dict[game.game_id] = game

    def remove_game_from_set_and_dict(self, game):
        self.current_games_id_set.remove(game.game_id)
        self.games_dict.pop(game.game_id)
