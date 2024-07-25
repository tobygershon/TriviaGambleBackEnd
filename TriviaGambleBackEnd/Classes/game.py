from random import randint
class Game:

# games also need different modes at some point
    def __init__(self, game_id):
        self.game_id = game_id
        self.has_started = False
        self.has_ended = False
        self.ending_score = 10
        self.player_list = []
        self.rounds_list = []
        self.winner = None
