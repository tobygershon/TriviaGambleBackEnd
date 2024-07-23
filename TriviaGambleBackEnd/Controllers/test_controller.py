from flask import Flask, jsonify, request
from flask_cors import CORS


# firestore package from python backend
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore


cred = credentials.Certificate('../firebase_service_account.json')

fire_base_app = firebase_admin.initialize_app(cred)
db = firestore.client()

# data = {"score": "0"}
#
# # Add a new doc in collection 'cities' with ID 'LA'
# db.collection("triviaGambleTesting").document("2").set(data)



# Set the capital field
def increment(request):
    doc_ref = db.collection("triviaGambleTesting").document("1")

    if request == 'true':
        doc_ref.update({"score": firestore.Increment(1)})
    elif request == 'false':
        doc_ref.update({"score": firestore.Increment(-1)})


# above is firestore code


app = Flask(__name__)
cors = CORS(app)


@app.route("/<answer>", methods=['GET', 'POST'])
def return_answer(answer):
    response = get_answer(answer)
    # response.headers.add('Access-Control-Allow-Origin', '*'
    return response


def get_answer(answer):
    if answer == 'true':
        resp = {'answer': True}
    elif answer == 'false':
        resp = {'answer': False}
    else:
        resp = {'answer': 'unknown'}

    return resp


@app.route("/question", methods=['POST'])
def respond_to_post():
    question = request.json
    response = {'q': question['q'].upper()}
    # response.headers.add('Access-Control-Allow-Origin', '*')
    return response


@app.route("/backend", methods=['POST'])
def update_db():
    post_req = request.json
    increment(post_req['val'])

    # the above receives a post request w/val of true or false
    # it calls increment method which in turn adds or subtracks one from firebase db based on the posted 'val'

    return {'status': 'success'}


if __name__ == "__main__":
    app.run()