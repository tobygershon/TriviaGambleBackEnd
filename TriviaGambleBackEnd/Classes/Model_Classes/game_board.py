import random as r
class GameBoard:

    def __init__(self):
        self.current_games_dict = {}


    def add_new_game_to_current_game_dict(self, game):
        self.current_games_dict[game.game_id] = game

    def remove_game_from_current_game_dict(self, game):
        self.current_games_dict.pop(game.game_id)
