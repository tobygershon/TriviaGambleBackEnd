

# Each Round has a dictionary of answers associated with it

def get_round_obj_for_firestore_db(category):
    return {
        "category": category,
        "isBetting": True,
        "highBet": {
            "bet": 0,
            "player": ""
        },
        "isOver": False,
        "answers": [],
        "wonRound": 'PENDING',
        "startNextRound": False
    }


class Round:

    def __init__(self, round_id, category):
        self.round_id = round_id
        self.category = category
        self.is_betting = True
        self.high_bet = None
        self.is_over = False
        self.answers_list = []



