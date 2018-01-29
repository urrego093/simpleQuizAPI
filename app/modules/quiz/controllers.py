from app.modules.quiz.models import Quiz, Question, Base
from app.modules.quiz.utils.quiz import quiz_helper
from flask import url_for, jsonify
from app.modules.quiz.db.db_controller import DbController


class Controller:
    def __init__(self):
        self.__db_controller = DbController()
        self.__db_controller.create_tables(Base)

    def get_new_quiz(self, name=None, description=None, question_count=20, max_score=10.0):
        """

        :param name:
        :param description:
        :param question_count:
        :param max_score:
        :return:
        """
        new_quiz = self.__db_controller.insert.create_quiz(name, description, question_count, max_score)
        return new_quiz

    def get_quiz(self, quiz_code):
        """

        :param quiz_code:
        :return:
        """
        quiz = self.__db_controller.consult.search_quiz(quiz_code)
        if quiz:
            return quiz_helper.to_json(quiz)
        else:
            return jsonify({'Error': "There is no Quiz with that code"})

    def update_quiz( self, quiz_data, quiz_code):
        # type: (object) -> object
        """

        :param quiz_data:
        :param quiz_code:
        :return:
        """

        quiz_received = quiz_helper.quiz_from_json(quiz_data)
        if quiz_received.code == quiz_code:
            new_quiz = self.__db_controller.update.update_quiz(quiz_received, quiz_code)
            if isinstance(new_quiz, Quiz):
                return quiz_helper.to_json(new_quiz)
            else:
                return jsonify({'Error': 'Too many results'})
        else:
            return jsonify({'Error': "The data received doesn't correspond to the quiz code."})

    def answer_quiz(self, quiz_data, quiz_code):
        """

        :param quiz_data:
        :param quiz_code:
        :return:
        """
        quiz_received = quiz_helper.quiz_from_json(quiz_data)
        if quiz_received.code == quiz_code:
            new_quiz = self.__db_controller.update.answer_quiz(quiz_received, quiz_code)
            if isinstance(new_quiz, Quiz):
                message = quiz_helper.to_json(new_quiz)
            else:
                message = jsonify({'Error': "The quiz specified doesn't exist."})
        else:
            message = jsonify({'Error': "The data received doesn't correspond to the quiz code."})

        return message

    def grade_quiz(self, quiz_code):
        """

        :param quiz_data:
        :param quiz_code:
        :return:
        """
        new_quiz = self.__db_controller.update.grade_quiz(quiz_code)
        if isinstance(new_quiz, Quiz):
            message = quiz_helper.to_json(new_quiz)
        else:
            message = jsonify({'Error': "The code received doesn't belongs to a quiz code."})

        return message
