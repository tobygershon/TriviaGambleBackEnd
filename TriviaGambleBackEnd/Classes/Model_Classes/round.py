import answer
import player

# Each Round has a dictionary of answers associated with it


class Round:

    def __init__(self, category):
        self.category = category
        self.is_betting = True
        self.high_bet = None
        self.is_over = False
        self.answers_list = []

    def get_round_obj_for_firestore_db(self):

        return {
            "category": self.category,
            "isBetting": True,
            "highBet": {
                "bet": 0,
                "player": ""
            },
            "isOver": False,
            "answers": [
                {
                    "answer": "",
                    "status": "PENDING",
                }
            ]
        }


