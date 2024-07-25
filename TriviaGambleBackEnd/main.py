from Classes import answer
from Controllers import test_controller as c
from Classes import game_board
from Classes import game
from Services import firebase_service as f

# new_answer = answer.Answer("Imbeed")
# new_answer.is_answer_correct()
#
# print(new_answer.is_correct)


def main():
    new_game_board = game_board.GameBoard()  # instantiate new board
    # then create new game in firestore and retrieve id, then instantiate new Game object and add to game board
    first_game_id = f.create_new_game_doc_in_firestore()
    print(first_game_id)
    first_game = game.Game(first_game_id)
    new_game_board.add_new_game_to_current_game_dict(first_game)
    print(first_game.game_id)
    c.app.run()  #run the flask application from the controller




if __name__ == "__main__":
    main()
