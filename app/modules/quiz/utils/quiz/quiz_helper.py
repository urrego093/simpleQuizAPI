import json
from app.modules.quiz.models import *


def to_json(quiz_input):
    """

    :param quiz_input:
    :return:
    """
    dictionary = dict()
    try:
        dictionary["code"] = quiz_input.code
        dictionary["uri"] = quiz_input.uri
        dictionary["name"] = quiz_input.name
        dictionary["description"] = quiz_input.description
        dictionary["score"] = quiz_input.score
        dictionary["score"] = quiz_input.score
        dictionary["max_score"] = quiz_input.max_score
        dictionary["question_count"] = quiz_input.question_count

        questions = []
        for question in quiz_input.questions:
            question_dict = dict()
            question_dict["uri"] = question.uri
            question_dict["code"] = question.code
            question_dict["text"] = question.text
            question_dict["score"] = question.score
            question_dict["max_score"] = question.max_score
            question_dict["option_count"] = question.option_count

            questions.append(question_dict)

            options = []
            for option in question.options:
                option_dict = dict()
                option_dict["uri"] = option.uri
                option_dict["code"] = option.code
                option_dict["text"] = option.text
                option_dict["score"] = option.score
                option_dict["is_correct"] = option.is_correct
                option_dict["is_selected"] = option.is_selected

                options.append(option_dict)

            question_dict["options"] = options

        dictionary["questions"] = questions

    except TypeError:
        print("The parameter send is not an instance of a Quiz")

    parent_dict = dict(quiz=dictionary)
    return json.dumps(parent_dict)


def quiz_from_json(json_input):
    """

    :param json_input:
    :return:
    """
    quiz_data = json.loads(json_input)["quiz"]
    new_quiz = Quiz()
    new_quiz.code = quiz_data["code"]
    new_quiz.description = quiz_data["description"]
    new_quiz.score = quiz_data["score"]
    new_quiz.max_score = quiz_data["max_score"]
    new_quiz.question_count = quiz_data["question_count"]
    new_quiz.name = quiz_data["name"]
    new_quiz.uri = quiz_data["uri"]

    question_array = quiz_data["questions"]
    questions = []
    for question_data in question_array:
        question = Question()
        question.code = question_data["code"]
        question.text = question_data["text"]
        question.uri = question_data["uri"]
        question.option_count = question_data["option_count"]
        question.score = question_data["score"]
        question.max_score = question_data["max_score"]

        option_array = question_data["options"]
        options = []
        for option_data in option_array:
            option = Option()
            option.code = option_data["code"]
            option.is_selected = option_data["is_selected"]
            option.text = option_data["text"]
            option.uri = option_data["uri"]
            option.is_correct = option_data["is_correct"]
            option.score = option_data["score"]

            options.append(option)  # here the option is appended to the question - options array

        question.options = options
        questions.append(question)  # here the question is appended to the quiz - questions array

    new_quiz.questions = questions

    return new_quiz


