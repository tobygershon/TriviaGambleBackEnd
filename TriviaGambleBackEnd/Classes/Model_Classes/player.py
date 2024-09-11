
# return model object for noSQL db
def get_player_obj_for_firestore_db(name):
    return {
        "name": name,
        "score": 0,
        "isJudge": False,
        "isAnswering": False,
        "isHighBet": False   # use this field to control betting turns from front end only
    }


class Player:

    def __init__(self, name, player_id):
        self.name = name
        self.player_id = player_id
        self.score = 0
        self.is_judge = False
        self.is_answering = False



