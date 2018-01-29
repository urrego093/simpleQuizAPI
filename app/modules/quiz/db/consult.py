from sqlalchemy.orm.exc import (NoResultFound, MultipleResultsFound)
from app.modules.quiz.models import Quiz


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

class Consult(object):
    __metaclass__ = Singleton

    def __init__(self, session):
        self.__session = session

    '''
        Search a quizz by ids code, could be improved to search any object
    '''
    def search_quiz(self, quiz_code):
        try:
            return self.__session.query(Quiz).filter_by(code=quiz_code).one()
        except NoResultFound:
            print "No result found"
            return None
