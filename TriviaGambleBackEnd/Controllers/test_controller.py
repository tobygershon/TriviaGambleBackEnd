from flask import Flask, jsonify


app = Flask(__name__)


@app.route("/<answer>", methods=['GET', 'POST'])
def return_answer(answer):
    response = jsonify(get_answer(answer))
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


def get_answer(answer):
    if answer == 'true':
        resp = {'answer': True}
    elif answer == 'false':
        resp = {'answer': False}
    else:
        resp = {'answer': 'unknown'}

    print(resp)
    return resp


if __name__ == "__main__":
    app.run()