import json
from flask import Flask, jsonify, abort, request
from modules.quiz.controllers import Controller
from modules.quiz.utils.data import get_str
from modules.quiz.utils.quiz import quiz_helper


app = Flask(__name__)
controller = Controller()


def run():
    app.run()

# @app.route('/quiz', methods=['GET', 'POST'])
# I was thinking about creating a quiz with name, description, max_score
# and number_of questions parametrized but didn't have the time
@app.route('/quiz', methods=['GET'])


def create_quiz():
    """
        A new instance of a quiz

    :return: json representing the quiz or with a custom error
    """
    # if request.method == 'POST':
    #    quiz_data = json.loads(request.get_json())["quiz"]
    #    name = quiz_data["name"]
    #    description = quiz_data["description"]
    #    new_quiz = controller.get_new_quiz(name=name, description=description, question_count=20, max_score=10.0)
    #    return quiz_helper.to_json(new_quiz)
    # else:'''
    new_quiz = controller.get_new_quiz(question_count=20, max_score=10.0)
    return quiz_helper.to_json(new_quiz)


@app.route('/quiz/<quiz_code>', methods=['GET'])
def get_quiz(quiz_code):
    """
    Get the selected quiz instance

    :param quiz_code:
    :return: json representing the quiz or with a custom error
    """
    message = controller.get_quiz(quiz_code)
    return message


@app.route('/quiz/<quiz_code>/update', methods=['PUT'])
def update_quiz(quiz_code):
    json_data = get_str(request.get_json())
    message = controller.update_quiz(json_data, quiz_code)
    return message


@app.route('/quiz/<quiz_code>/answer', methods=['PUT'])
def answer(quiz_code):
    """
    Updates the quiz instance with the information received as json

    :param quiz_code:
    :return: json representing the quiz or with a custom error
    """
    json_data = get_str(request.get_json())
    text_response = controller.answer_quiz(json_data, quiz_code)
    return text_response


@app.route('/quiz/<quiz_code>/grade', methods=['get'])
def grade(quiz_code):
    """
    Grades the instance according to the options selected using the answer method

    :param quiz_code:
    :return: json representing the quiz or with a custom error
    """
    text_response = controller.grade_quiz(quiz_code)
    return text_response

if __name__ == '__main__':
    app.run()


@app.errorhandler(404)
def not_found(error):
        return jsonify({'error': 'Not found'})


@app.errorhandler(405)
def too_many(error):
        return jsonify({'error': 'Too many results'})