from Services import chat_completions as c
# Each answer has an ordered number associated with it and the str of the answer and boolean is_correct
class Answer:

    def __init__(self, answer):
        self.answer = answer
        self.status = 'PENDING'

    def is_answer_correct(self):
        completion = c.ChatQuery()
        answer = completion.query_for_answer("Philadelphia 76ers players who played with Allen Iverson", self.answer)

        if answer == 'y':
            self.is_correct = True
        elif answer == 'n':
            pass
        else:
            # throw error in this case
            pass




