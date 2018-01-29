from sqlalchemy.orm.exc import (NoResultFound, MultipleResultsFound)
from app.modules.quiz.models import Quiz
import itertools


class Singleton(type):

    def __init__(cls,name, bases, dict):
        super(Singleton, cls).__init__(name, bases, dict)
        cls.instance = None

    def __call__(cls, *args, **kwargs):
        if cls.instance is None:
            cls.instance = super(Singleton, cls).__call__(*args, **kwargs)
        else:
            cls._instances[cls].__init__(*args, **kwargs)

        return cls.instance


class Update(object):
    __metaclass__ = Singleton

    def __init__(self, session):
        self.__session = session

    def update_quiz(self, quiz_received, quiz_code):
        # type: (object) -> object

        try:
            quiz_found = self.__session.query(Quiz).filter_by(code=quiz_code).one()

            quiz_found.name = quiz_received.name
            quiz_found.description = quiz_received.description
            quiz_found.max_score = quiz_received.max_score

            new_max_score_per_question = quiz_found.max_score / quiz_found.question_count

            questions_received = quiz_received.questions
            questions_found = quiz_found.questions
            questions_iterator = [questions_received, questions_found]

            for question_received, question_found in itertools.product(*questions_iterator):
                if question_received.code == question_found.code:
                    question_found.text = question_received.text
                    question_found.max_score = new_max_score_per_question
                    question_found.score = 0.0

                    options_received = question_received.options
                    options_found = question_found.options
                    options_iterator = [options_received, options_found]

                    for option_received, option_found in itertools.product(*options_iterator):
                        if option_received.code == option_found.code:
                            option_found.text = option_received.text
                            option_found.is_correct = option_received.is_correct
                            option_found.is_selected = option_received.is_selected

            return quiz_found
        except NoResultFound:
            print "Quiz of code {} not found.".format(quiz_code)
            return "-"

    def answer_quiz(self, quiz_received, quiz_code):
        try:
            quiz_found = self.__session.query(Quiz).filter_by(code=quiz_code).one()

            questions_received = quiz_received.questions
            questions_found = quiz_found.questions
            questions_iterator = [questions_received, questions_found]

            for question_received, question_found in itertools.product(*questions_iterator):
                if question_received.code == question_found.code:
                    options_received = question_received.options
                    options_found = question_found.options
                    options_iterator = [options_received, options_found]

                    for option_received, option_found in itertools.product(*options_iterator):
                        if option_received.code == option_found.code:
                            option_found.is_selected = option_received.is_selected

            return quiz_found
        except NoResultFound:
            print "Quiz of code {} not found.".format(quiz_code)
            return "-"

    def grade_quiz(self, quiz_code):
        try:
            quiz = self.__session.query(Quiz).filter_by(code=quiz_code).one()
            total_score = 0.0

            questions = quiz.questions

            for question in questions:
                options = question.options
                for option in options:
                    if option.is_selected and option.is_correct:
                        question.score = question.max_score
                total_score = total_score + question.score

            quiz.score = total_score

            return quiz
        except NoResultFound:
            print "Quiz of code {} not found.".format(quiz_code)
            return "-"
