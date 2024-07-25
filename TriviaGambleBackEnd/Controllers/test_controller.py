from flask import Flask, jsonify, request
from flask_cors import CORS
from Services import firebase_service as f


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
    f.increment(post_req['val'])

    # the above receives a post request w/val of true or false
    # it calls increment method which in turn adds or subtracks one from firebase db based on the posted 'val'

    return {'status': 'success'}


@app.route("/game", methods=['POST'])
def create_new_game():
    new_game_id = f.create_new_game_doc_in_firestore()
    return {"new_game_id": new_game_id}


