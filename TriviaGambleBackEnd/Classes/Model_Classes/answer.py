from Services import chat_completions as c
# Each answer has an ordered number associated with it and the str of the answer and boolean is_correct


class Answer:

    def __init__(self, answer):
        self.answer = answer
        self.status = 'PENDING'

    def get_answer_obj_for_firestore_db(self):
        return {
            "answer": self.answer,
            "status": self.status
        }

    def is_answer_correct(self):
        completion = c.ChatQuery()
        answer = completion.query_for_answer_with_3_turbo("Philadelphia 76ers players who played with Allen Iverson", self.answer)

        if answer == 'y':
            self.status = True
        elif answer == 'n':
            self.status = False
        else:
            # throw error in this case
            pass




