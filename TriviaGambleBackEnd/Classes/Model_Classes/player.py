

class Player:

    def __init__(self, name):
        self.name = name
        self.score = 0
        self.is_judge = False
        self.is_answering = False

    # return model object for noSQL db
    def get_player_obj_for_firestore_db(self):
        return {
                "name": self.name,
                "score": 0,
                "isJudge": False,
                "isAnswering": False,
                "isHighBet": False   # use this field to control betting turns from front end only
            }
