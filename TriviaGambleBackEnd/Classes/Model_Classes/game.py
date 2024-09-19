import random as r
from Services import firebase_service as f
from Classes.Model_Classes import player
from Classes.Model_Classes import round
from Classes.Model_Classes import bet
from Classes.Model_Classes import answer


def get_game_obj_for_firestore_db(chat_id):
    return {
        "hasStarted": False,
        "hasEnded": False,
        "gamePhase": "beforeStart",
        "endingScore": 10, # is this necessary on front end/db?
        "winner": "",
        "players": [],
        "rounds": [],
        "chat": chat_id
    }


class Game:

    # games also need different modes at some point
    def __init__(self, game_id):
        self.game_id = game_id
        self.has_started = False
        self.has_ended = False
        self.game_phase = "beforeStart"
        self.ending_score = 10
        self.player_list = []
        self.rounds_list = []
        self.winner = None
        self.judge_index = 0

    def add_player(self, player_name):
        # first create player doc in db to get player doc id back
        player_id = f.create_new_player_doc_in_firestore(player_name)

        # create new player obj and add to player list of game
        new_player = player.Player(player_name, player_id)
        self.player_list.append(new_player)

        # add returned player docId to game players array
        f.update_firestore_array(self.game_id, "games", "add", "players", new_player.player_id)

        return player_id

    def start_game(self):
        # randomly shuffle player list order
        r.shuffle(self.player_list)

        # update is_judge for players.  index 0 starts as judge
        self.player_list[self.judge_index].is_judge = True
        f.update_firestore_field(self.player_list[self.judge_index].player_id, "players", "isJudge", True)

        #update has_started for obj and db
        self.has_started = True
        self.update_game_phase("gameStarting")
        f.update_firestore_field(self.game_id, "games", "hasStarted", True)

    def update_game_phase(self, new_phase):
        self.game_phase = new_phase
        f.update_firestore_field(self.game_id, "games", "gamePhase", new_phase)

    def add_round(self, category):
        #first create new round doc in db to get round doc id back
        round_id = f.create_new_round_doc_in_firestore(category)

        # create new round obj and add round to game's rounds list
        new_round = round.Round(round_id, category)
        self.rounds_list.append(new_round)

        # add round doc ID to rounds array of game in db
        f.update_firestore_array(self.game_id, "games", "add", "rounds", new_round.round_id)
        # update game phase to startBetting
        self.update_game_phase("startBetting")

        return round_id

    def set_high_bet(self, high_bet_player_id, high_bet):
        # create high bet obj
        high_bet_player = None
        # high_bet_player = [p.player_id == high_bet_player_id for p in self.player_list] correct?
        for p in self.player_list:
            if p.player_id == high_bet_player_id:
                high_bet_player = p

        if high_bet_player:
            high_bet_obj = bet.Bet(high_bet_player, high_bet)

            # add bet obj to high_bet for current round and change is betting to false
            self.get_current_round_object().high_bet = high_bet_obj
            self.get_current_round_object().is_betting = False

            # update isBetting and highBet in db with one call for round doc
            bet_to_add = high_bet_obj.get_bet_obj_for_firestore_db()
            f.update_2_firestore_fields(self.get_current_round_object().round_id, "rounds", "highBet", bet_to_add, "isBetting", False)

            # update player with isAnswering (resetting of isHighBet to false for next round is at end of round)
            high_bet_player.is_answering = True
            f.update_firestore_field(high_bet_player.player_id, "players", "isAnswering", True)

            # update phase to endBetting
            self.update_game_phase("endBetting")

        else:
            # throw error?
            print("no high bet player")
            pass

    def add_answer(self, submitted_answer):
        # first add new answer doc to db and get returned Id
        returned_answer_id = f.create_new_answer_doc_in_firestore(submitted_answer)

        # create new answer obj
        new_answer = answer.Answer(returned_answer_id, submitted_answer)

        # add answer to current round's list
        self.get_current_round_object().answers_list.append(new_answer)
        f.update_firestore_array(self.get_current_round_object().round_id, "rounds",
                                 "add","answers", new_answer.answer_id)

        # if chat_completions is getting result, it should be called here

    def update_answer_status(self, answer_id, updated_status):
        answer_to_update = None
        for a in self.get_current_round_object().answers_list:
            if a.answer_id == answer_id:
                answer_to_update = a

        if answer_to_update:
            answer_to_update.status = updated_status
            f.update_firestore_field(answer_to_update.answer_id, "answers", "status", answer_to_update.status)
        else:
            # throw error?
            pass

    def check_if_round_won(self):
        # compare correct responses with high bet, and update score and db if high bet met
        if self.get_count_of_correct_answers() == self.get_current_round_object().high_bet.bet:
            return True
        else:
            return False

    def end_round(self, won_round):
        self.update_scores(won_round=won_round)
        self.update_round_over()

        # check if game is over
        if self.check_if_game_over():
            #update hasEnded, winner.
            if len(self.get_winner()) == 1:
                self.winner = self.get_winner()[0]
                self.has_ended = True
                # update both fields in one call
                f.update_2_firestore_fields(self.game_id, "games", "winner", self.winner.player_id, "hasEnded", True)
                self.update_game_phase("gameEnding")
            else:
                # tiebraker?
                pass

    def start_next_round(self):
        # change isJudge to false for current judge
        self.player_list[self.judge_index].is_judge = False
        f.update_firestore_field(self.player_list[self.judge_index].player_id, "players","isJudge", False)

        # next increment game's judge index
        if self.judge_index + 1 == len(self.player_list):
            self.judge_index = 0
        else:
            self.judge_index += 1

        self.player_list[self.judge_index].is_judge = True
        f.update_firestore_field(self.player_list[self.judge_index].player_id, "players", "isJudge", True)

        # change isAnswering to false and isHighBet to false in firestore db
        answering_player = self.get_current_round_object().high_bet.player
        answering_player.is_answering = False
        f.update_2_firestore_fields(answering_player.player_id, "players", "isAnswering", False, "isHighBet", False)

        # change startNextRound to true in current round in firestore to trigger change of phase back to beginning
        f.update_firestore_field(self.get_current_round_object().round_id, "rounds", "startNextRound", True)


    # Helper Methods

    def get_count_of_correct_answers(self):
        current_answers_list = self.get_current_round_object().answers_list

        current_correct_answers = sum(a.status is True for a in current_answers_list)

        return current_correct_answers

    def check_if_enough_answers_pending(self):
        current_answers_list = self.get_current_round_object().answers_list
        count_pending_answers = 0
        count_correct_answers = self.get_count_of_correct_answers()
        current_round = self.get_current_round_object()
        high_bet = current_round.high_bet.bet

        for a in current_answers_list:
            if a.status in ('PENDING', 'APPEALED') :
                count_pending_answers += 1

        if count_pending_answers + count_correct_answers >= high_bet:
            return True
        else:
            return False


    def get_current_round_object(self):
        if len(self.rounds_list) > 0:
            return self.rounds_list[-1]
        # else throw error?

    # def get_index_of_current_round(self):
    #     if len(self.rounds_list) > 0:
    #         return len(self.rounds_list) - 1
    #     # else throw an error?
    #
    # def get_index_of_player(self, search_player):
    #     for x in range(len(self.player_list)):
    #         if self.player_list[x].name == search_player.name:
    #             return x

    def get_index_of_next_judge(self):
        for x in range(len(self.player_list)):
            if self.player_list[x].is_judge:
                index_next_judge = x + 1
                print(f'{x} is the current judge index')
                print(f'{index_next_judge} is the returned next_judge index')
                return index_next_judge

    def get_other_players(self):
        other_players_list = []

        for p in self.player_list:
            if not p.is_judge and not p.is_answering:
                other_players_list.append(p)

        return other_players_list

    def update_round_over(self):
        # update round is over
        f.update_firestore_field(self.get_current_round_object().round_id, "rounds", "isOver", True)
        #update phase
        self.update_game_phase("endAnswering")

    def update_scores(self, won_round):

        if won_round:
            winning_player = self.get_current_round_object().high_bet.player
            winning_player.score += 1
            f.increment(winning_player.player_id, "players", "score")
            f.update_firestore_field(self.get_current_round_object().round_id, "rounds", "wonRound", True)
        else:
            f.update_firestore_field(self.get_current_round_object().round_id, "rounds", "wonRound", False)
            other_players_list = self.get_other_players()
            for p in other_players_list:
                p.score += 1
                f.increment(p.player_id, "players", "score")

    def check_if_game_over(self):
        is_over = False

        for p in self.player_list:
            if p.score == self.ending_score:
                is_over = True
                break

        return is_over

    def get_winner(self):
        # create list to return b/c possible for more than one person reach final score at same time if more than 3 people playing
        winner_list = []
        for p in self.player_list:
            if p.score == self.ending_score:
                winner_list.append(p)

        return winner_list

