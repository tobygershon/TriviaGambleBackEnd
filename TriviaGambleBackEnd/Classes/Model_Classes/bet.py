class Bet:

    def __init__(self, player, bet):
        self.player = player
        self.bet = bet

    def get_bet_obj_for_firestore_db(self):
        return {
            "bet": self.bet,
            "player": self.player.name
        }