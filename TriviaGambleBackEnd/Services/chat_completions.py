from openai import OpenAI

class ChatQuery:

    def __init__(self):
        self.client = OpenAI()


    # method to query chatgpt for yes or no response

    def query_for_answer_with_3_turbo(self, topic, answer):
        completion = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system",
                 "content": f"You are a trivia judge.  You are very lenient with spelling errors and capitalization especially with names of people and places.  You need to determine whether the user's answer is valid for the current topic of '{topic}'.  Only accept single names for people if they are not very common names.  You respond to the prompts with only yes or no as your answer."},
                {"role": "user",
                 "content": f"does '{answer}' correctly belong in a list of answers for the current topic of '{topic}'? yes or no?"}
            ]
        )
        print(completion.choices[0].message.content[0].lower())
        return completion.choices[0].message.content[0].lower()


    # look into 4o-mini as new model
    def query_for_answer_with_4o(self, topic, answer):
        completion = self.client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": f"You are a trivia judge.  You are very lenient with spelling errors and capitalization especially with names of people and places.  You need to determine whether the user's answer is valid for the current topic of '{topic}'.  Only accept single names for people if they are not very common names.  You respond to the prompts with only yes or no as your answer."},
                {"role": "user", "content": f"does '{answer}' correctly belong in a list of answers for the current topic of '{topic}'? yes or no?"}
            ]
        )
        print(completion.choices[0].message.content[0].lower())
        return completion.choices[0].message.content[0].lower()