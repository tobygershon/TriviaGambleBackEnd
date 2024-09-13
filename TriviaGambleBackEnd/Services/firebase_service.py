import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from Classes.Model_Classes import game
from Classes.Model_Classes import player
from Classes.Model_Classes import round
from Classes.Model_Classes import answer
from Classes.Model_Classes import chat

cred = credentials.Certificate('./firebase_service_account.json')

fire_base_app = firebase_admin.initialize_app(cred)
db = firestore.client()


def create_new_game_doc_in_firestore(chat_id):

    model_game = game.get_game_obj_for_firestore_db(chat_id)

    try:
        update_time, game_ref = db.collection("games").add(model_game)
        # update_time gives timestamp of creation
    except Exception:
        print("create new game in firestore failed")
        return None
    else:
        return game_ref.id


def create_new_player_doc_in_firestore(player_name):

    model_player = player.get_player_obj_for_firestore_db(player_name)

    try:
        update_time, player_ref = db.collection("players").add(model_player)
        # update_time gives timestamp of creation
    except Exception:
        print("create new player in firestore failed")
        return None
    else:
        return player_ref.id


def create_new_round_doc_in_firestore(category):

    model_round = round.get_round_obj_for_firestore_db(category)

    try:
        update_time, round_ref = db.collection("rounds").add(model_round)
        # update_time gives timestamp of creation
    except Exception:
        print("create new round in firestore failed")
        return None
    else:
        return round_ref.id


def create_new_answer_doc_in_firestore(submitted_answer):

    model_answer = answer.get_answer_obj_for_firestore_db(submitted_answer)

    try:
        update_time, answer_ref = db.collection("answers").add(model_answer)
        # update_time gives timestamp of creation
    except Exception:
        print("create new answer in firestore failed")
        return None
    else:
        return answer_ref.id


def create_new_chat_doc_in_firestore():

    model_chat = chat.get_chat_obj_for_firestore_db()

    try:
        update_time, answer_ref = db.collection("chats").add(model_chat)
    except Exception:
        print("create new chat in firestore failed")
    else:
        return answer_ref.id

def update_firestore_field(doc_id, collection, field_to_update, updated_value):
    try:
        game_ref = db.collection(collection).document(doc_id)

        game_ref.update({field_to_update: updated_value})
    except Exception:
        print("Update field in firestore failed")
        return False
    else:
        return True


def update_2_firestore_fields(doc_id, collection, field_1_to_update, updated_value_1, field_2_to_update, updated_value_2):
    try:
        game_ref = db.collection(collection).document(doc_id)

        game_ref.update({
            field_1_to_update: updated_value_1,
            field_2_to_update: updated_value_2
        })
    except Exception:
        print("Update field in firestore failed")
        return False
    else:
        return True

def update_firestore_array(doc_id, collection, add_or_remove_element, field_to_update, updated_value):
    try:
        game_ref = db.collection(collection).document(doc_id)

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


def increment(doc_id, collection, field_to_incremented):
    try:
        game_ref = db.collection(collection).document(doc_id)
        game_ref.update({field_to_incremented: firestore.Increment(1)})
    except Exception:
        print("increment field in firestore failed")
        return False
    else:
        return True
