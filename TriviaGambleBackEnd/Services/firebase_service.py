import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.Certificate('./firebase_service_account.json')

fire_base_app = firebase_admin.initialize_app(cred)
db = firestore.client()


def create_new_game_doc_in_firestore():
    model_game = {
        "hasStarted": False,
        "hasEnded": False,
        "endingScore": 10, # is this necessary on front end/db?
        "winner": "",
        "players": [],
        "rounds": []
    }

    try:
        update_time, game_ref = db.collection("triviaGambleTesting").add(model_game)
        # update_time gives timestamp of creation
    except Exception:
        print("create new game in firestore failed")
        return None
    else:
        return game_ref.id


def update_firestore_game_field(game_id, field_to_update, updated_value):
    try:
        game_ref = db.collection("games").document(game_id)

        game_ref.update({field_to_update: updated_value})
    except Exception:
        print("Update field in firestore failed")
        return False
    else:
        return True


def update_firestore_game_array(game_id, add_or_remove_element, field_to_update, updated_value):
    try:
        game_ref = db.collection("games").document(game_id)

        if add_or_remove_element == "add":
            game_ref.update({field_to_update: firestore.ArrayUnion([updated_value])})
        elif add_or_remove_element == "remove":
            # unclear if update_value below should be entire player object to remove or index of array?
            game_ref.update({field_to_update: firestore.ArrayRemove([updated_value])})
        else:
            print("add_or_remove value was invalid")
    except Exception:
        print("Update array field in firestore failed")
        return False
    else:
        return True


def increment(game_id, field_to_incremented):
    try:
        game_ref = db.collection("games").document(game_id)
        game_ref.update({field_to_incremented: firestore.Increment(1)})
    except Exception:
        print("increment field in firestore failed")
        return False
    else:
        return True
