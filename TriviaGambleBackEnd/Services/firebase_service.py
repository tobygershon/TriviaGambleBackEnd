import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.Certificate('./firebase_service_account.json')

fire_base_app = firebase_admin.initialize_app(cred)
db = firestore.client()


def create_new_game_doc_in_firestore():
    game = {"players": ['toby', 'huy', 'pete'], "hasStarted": False, "hasEnded": False}
    update_time, city_ref = db.collection("triviaGambleTesting").add(game)
    # update_time gives timestamp of creation
    return city_ref.id


def increment(request):
    doc_ref = db.collection("triviaGambleTesting").document("1")

    if request == 'true':
        doc_ref.update({"score": firestore.Increment(1)})
    elif request == 'false':
        doc_ref.update({"score": firestore.Increment(-1)})
