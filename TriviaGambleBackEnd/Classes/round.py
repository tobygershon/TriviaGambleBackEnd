import answer
import player

# Each Round has a dictionary of answers associated with it

class Round:

    def __init__(self):
        self.category = None
        self.is_over = False
        self.high_bet = None
        self.answers_dict = []


