from random import randint
class Game:

    def __init__(self, player1, player2, player3, winning_score):
        self.game_id = randint(10000, 999999)
        self.player_tuple = (player1, player2, player3)
        self.winning_score = winning_score
        self.is_over = False
        self.rounds_list = []