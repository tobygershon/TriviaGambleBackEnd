from flask import Flask, jsonify, request
from flask_cors import CORS
from Services import firebase_service as f


app = Flask(__name__)
cors = CORS(app)


# routes for creating game (in case someone inviting others to play)

@app.post("/new_game")
def create_new_game():
# create new game object
# add creating player
# update db
    new_game_id = f.create_new_game_doc_in_firestore()
# return gameId to navigate front end
    return {"new_game_id": new_game_id}


# routes for game initialization

# adding players
@app.put("/<game_id>/add_player")
def add_player_to_game(game_id):
# get game
    # add player to game object
    # check if game is full and update game object and firebase DB accordingly
         # Round 1 needs to be added
         # players need to be updated with isPlayersTurn to choose category
         # etc...
    # return game_id?  maybe not necessary since id already exists on front end to navigate player to


# routes for choosing category
@app.put("/<game_id>/category")
def add_category(game_id):
# get game
    # add category to current round (round in put request? or current round is last element in list?)
    # update db with various booleans to control front end


# routes for betting
@app.put("/<game_id>/bet")
def add_bet(game_id):
# get game
    # get bet from request object and compare to high bet
    # update db accordingly

@app.put("/<game_id>/end_betting")
def end_betting(game_id):
# get game
    # determine player and winning bet
    # update db with isAnswering boolean for player along with winning bet

# routes for answering
@app.put("/<game_id>/answer")
def submit_answer(game_id):
# get game
    # add answer to round and db first with 'pending' result?
    # if chatgpt is judge:
        # check answer
        # update answer with 'correct' or 'incorrect'
        # update db with result
        # compare correct responses with high bet, and update score and db if high bet met
        # check if game won, if not, update game and db for next round
    # if other players are judge
        # wait for their judgements


@app.put("/<game_id>/judge")
def submit_judgment_of_answer(game_id):
# request body will need to include answer number as well as judgement
    # update game with judgement
    # compare correct responses with high bet, and update score and db if high bet met
    # check if game won, if not, update game and db for next round

@app.put("/<game_id>/end_round")
def end_round(game_id):
# this endpoint is called when timer expires on front end with player loosing round
    # game/round/score updated both ends
    # check if game won, if not, update game and db for next round

@app.put("/<game_id>/dispute")
def dispute_answer(game_id):
# perhaps check for disputes after all rounds end, before updating scores, etc.
    # request body will need the answer number that is disputed
    # db updated with 'pending' or 'disputed' status for answer
    # unclear how to resolve disputes



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






