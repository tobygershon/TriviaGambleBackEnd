from flask import Flask, request
from flask_cors import CORS
from Services import firebase_service as f
from Classes.Model_Classes import game_board
from Classes.Model_Classes import game

app = Flask(__name__)
cors = CORS(app)

# When flask is run, new game board is created

new_game_board = game_board.GameBoard()  # instantiate new board
# then create new game in firestore and retrieve id, then instantiate new Game object and add to game board
first_game_id = f.create_new_game_doc_in_firestore()
print(first_game_id)
first_game = game.Game(first_game_id)
new_game_board.add_new_game_to_current_game_dict(first_game)
print(first_game.game_id)


# routes for creating game (in case someone inviting others to play)


@app.get("/")
def home_page():
    return {"valid_game": True}


@app.post("/new_game")
def create_new_game():
    # create new game in db
    new_game_id = f.create_new_game_doc_in_firestore()

    # create new game object
    new_game = game.Game(new_game_id)

    # add game to game_board
    new_game_board.add_new_game_to_current_game_dict(new_game)

    # add creating player to game and update db if player exists in post request
    first_player = request.json["player"]
    if first_player:
        player_id = new_game.add_player(first_player)
    else:
        player_id = None

    # return gameId to navigate front end
    return {"new_game_id": new_game_id,
            "player_id": player_id}


# routes for game initialization

# adding players
@app.put("/<game_id>/add_player")
def add_player_to_game(game_id):

    # get game
    game_to_update = new_game_board.current_games_dict[game_id]

    if game_to_update is not None:
        # add player to game object
        new_player = request.json["player"]
        returned_player_id = game_to_update.add_player(new_player)

        # check if game is full and update game object and firebase DB accordingly
        num_of_players = len(game_to_update.player_list)
        if num_of_players == 3:

            # start game
            game_to_update.start_game()

        return {'valid_game': True,
                'player_id': returned_player_id}

    else:
        print("gameID does not exist")
        return {'valid_game': False}


# routes for choosing category
@app.put("/<game_id>/category")
def add_category(game_id):
    # get game
    game_to_update = new_game_board.current_games_dict[game_id]

    if game_to_update is not None:
        # add new round with category
        new_category = request.json["category"]
        game_to_update.add_round(new_category)
        return {'valid_game': True}

    else:
        print("gameId does not exist")
        return {'valid_game': False}


# routes for betting
# maybe control betting from front end?
# timer will be from front end so highBet for round can be updated from front end until end of betting
@app.put("/<game_id>/bet")
def add_bet(game_id):
    # get game
    # get bet from request object and compare to high bet
    # update db accordingly
    pass


@app.put("/<game_id>/end_betting")
def end_betting(game_id):
    # get game
    game_to_update = new_game_board.current_games_dict[game_id]

    if game_to_update is not None:
        # request obj contains player id of high better and value of the bet
        game_to_update.set_high_bet(request.json["player"], request.json["bet"])

        return {'valid_game': True}
    else:
        print("gameId does not exist")
        return {'valid_game': False}


# routes for answering
@app.put("/<game_id>/answer")
def submit_answer(game_id):
    # get game
    game_to_update = new_game_board.current_games_dict[game_id]

    if game_to_update is not None:
        # add answer to round and db first with 'pending' result?
        game_to_update.add_answer(request.json["answer"])
        # if chatgpt is judge:
            # check answer
            # update answer with 'correct' or 'incorrect'
            # update db with result
            # compare correct responses with high bet, and update score and db if high bet met
            # check if game won, if not, update game and db for next round
        # if other players are judge
            # wait for their judgements
        return {'valid_game': True}
    else:
        print("gameId does not exist")
        return {'valid_game': False}

@app.put("/<game_id>/judge")
def submit_judgment_of_answer(game_id):
    # get game
    game_to_update = new_game_board.current_games_dict[game_id]

    if game_to_update is not None:
        # request body will need to include answer index as well as judgement
        game_to_update.update_answer_status(request.json["answer_id"], request.json["status"])

        # check if round won
        if game_to_update.check_if_round_won():
            game_to_update.end_round(won_round=True)

        return {'valid_game': True}

    else:
        print("gameId does not exist")
        return {'valid_game': False}

@app.put("/<game_id>/end_round")
def end_round(game_id):
    # this endpoint is called when timer expires on front end.  answers may still be pending
    # get game
    game_to_update = new_game_board.current_games_dict[game_id]

    if game_to_update is not None:
        if game_to_update.check_if_round_won():
            game_to_update.end_round(won_round=True)
        elif game_to_update.check_if_enough_answers_pending():
            return {'valid_game': True,
                    'status': 'PENDING'}
        else:
            game_to_update.end_round(won_round=False)

        return {'valid_game': True}
    else:
        print("gameId does not exist")
        return {'valid_game': False}


@app.put("/<game_id>/dispute")
def dispute_answer(game_id):
    # perhaps check for disputes after all rounds end, before updating scores, etc.
    # request body will need the answer number that is disputed
    # db updated with 'pending' or 'disputed' status for answer
    # unclear how to resolve disputes
    pass



# Below is testing methods

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






