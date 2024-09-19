import random as r


class GameBoard:

    def __init__(self):
        self.current_games_dict = {}

    def add_new_game_to_current_game_dict(self, game):
        self.current_games_dict[game.game_id] = game

    def remove_game_from_current_game_dict(self, game):
        self.current_games_dict.pop(game.game_id)

    def get_game(self, game_id):
        # get game
        game_to_update = self.current_games_dict[game_id]

        if game_to_update is not None:
            return game_to_update

        else:
            print("gameId does not exist")
            return False

    def get_all_unstarted_games(self):
        unstarted_games = []
        for game_id in self.current_games_dict:
            game = self.get_game(game_id)
            if not game.has_started:
                unstarted_games.append(game_id)

        return unstarted_games
