import random as r
from Services import firebase_service as f
from Classes.Model_Classes import player
from Classes.Model_Classes import round
from Classes.Model_Classes import bet
from Classes.Model_Classes import answer


class Game:

    # games also need different modes at some point
    def __init__(self, game_id):
        self.game_id = game_id
        self.has_started = False
        self.has_ended = False
        self.ending_score = 10
        self.player_list = []
        self.rounds_list = []
        self.winner = None

    def add_player(self, player_name):

        # create new player obj and add to player list of game
        new_player = player.Player(player_name)
        self.player_list.append(new_player)

        # add player obj to db
        player_obj = new_player.get_player_obj_for_firestore_db()
        f.update_firestore_game_array(self.game_id, "add", "players", player_obj)

    def add_round(self, category):

        # create new round obj and add round to game's rounds list
        new_round = round.Round(category)
        self.rounds_list.append(new_round)

        # add round obj to db
        round_obj = new_round.get_round_obj_for_firestore_db()
        f.update_firestore_game_array(self.game_id, "add", "rounds", round_obj)

    def start_game(self):
        # randomly shuffle player list order? how to update db with order?
        # r.shuffle(self.player_list)

        #update has_started for obj and db
        self.has_started = True
        f.update_firestore_game_field(self.game_id, "hasStarted", True)

        # update is_judge for players (for now index 0 starts as judge) unclear is accessing isJudge is correct with array
        self.player_list[0].is_judge = True
        f.update_firestore_game_field(self.game_id, "players[0].isJudge", True)

    def set_high_bet(self, player_index, high_bet):
        # create high bet obj
        high_bet_player = self.player_list[player_index]
        high_bet_obj = bet.Bet(high_bet_player, high_bet)

        # add bet obj to high_bet for current round
        self.get_current_round_object().high_bet = high_bet_obj

        bet_to_add = high_bet_obj.get_bet_obj_for_firestore_db()
        f.update_firestore_game_field(self.game_id, f'rounds[{self.get_index_of_current_round()}].highBet', bet_to_add)

        # update isBetting
        self.get_current_round_object().is_betting = False
        f.update_firestore_game_field(self.game_id, f'rounds[{self.get_index_of_current_round()}].isBetting', False)

        # update player with isAnswering
        high_bet_player.is_answering = True
        f.update_firestore_game_field(self.game_id, f'players[{player_index}].isAnswering', True)

    def add_answer(self, submitted_answer):
        # create new answer obj
        new_answer = answer.Answer(submitted_answer)

        # add answer to current round's list
        self.get_current_round_object().answers_list.append(new_answer)
        f.update_firestore_game_array(self.game_id, "add",
                                      f'rounds[{self.get_index_of_current_round()}].answers',
                                      new_answer.get_answer_obj_for_firestore_db())

        # if chat_completions is getting result, it should be called here

    def update_answer_status(self, answer_index, updated_status):
        answer_to_update = self.get_current_round_object().answers_list[answer_index]
        answer_to_update.status = updated_status

        f.update_firestore_game_array(self.game_id, "add",
                                      f'rounds[{self.get_index_of_current_round()}].answers[{answer_index}].status',
                                      answer_to_update.status)

    def check_if_round_won(self):
        # compare correct responses with high bet, and update score and db if high bet met
        if self.get_count_of_correct_answers() == self.get_current_round_object().high_bet.bet:
            return True
        else:
            return False

    def check_if_answers_pending(self):
        pass

    def update_round_over(self):
        # update round is over
        f.update_firestore_game_field(self.game_id, f'rounds[{self.get_index_of_current_round()}].isOver', True)

    def update_round_won(self):
        # update score
        # f.increment(self.game_id, "")
        pass

    def update_round_lost(self):
        pass

    def end_round(self):
        self.update_round_over()
        # determine points update
        # update new judge
        pass

    # Helper Methods

    def get_current_round_object(self):
        return self.rounds_list[-1]

    def get_index_of_current_round(self):
        return len(self.rounds_list) - 1

    def get_count_of_correct_answers(self):
        current_answers_list = self.get_current_round_object().answers_list

        current_correct_answers = sum(a.status is True for a in current_answers_list)


