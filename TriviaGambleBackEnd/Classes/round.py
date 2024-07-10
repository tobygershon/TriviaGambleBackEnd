import answer
import player

# Each Round has a dictionary of answers associated with it

class Round:

    def __init__(self, number, high_bet, player):
        self.number = number
        self.high_bet = high_bet
        self.player = player
        self.answers_dict = {}


