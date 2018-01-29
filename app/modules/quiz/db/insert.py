from app.modules.quiz.models import Quiz, Question, Option
import random


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

class Insert(object):
    __metaclass__ = Singleton

    def __init__(self, session):
        self.quiz_id_seq = 0
        self.question_id_seq = 0
        self.option_id_seq = 0
        self.__session = session


    '''
        
    '''
    def create_quiz(self, name, description, question_count, max_score):
        new_id = self.__get_next_quiz_id()
        code = "C-" + str(new_id)

        if name is None and description is None:
            new_quiz = Quiz(
                id=new_id, uri="-", code=code, name="New Quiz name.", description="New  Quiz description.",
                score=0.0, question_count=question_count, max_score=max_score
            )
        else:
            new_quiz = Quiz(
                id=new_id, uri="-", code=code, name=name, description=description,
                score=0.0, question_count=0, max_score=10.0
            )

        self.create_questions(new_quiz, question_count, max_score)
        self.__session.add(new_quiz)
        self.__session.commit()
        return new_quiz

    '''
        Creates {question_count} number of questions to the quiz 
    '''
    def create_questions(self, quiz, question_count, quiz_max_score):

        if isinstance(quiz, Quiz) is False:
            print("The parameter quiz is not an instance of Quiz.")
            return "Couldn't create the questions for an unknown Quiz."

        if isinstance(question_count, int) is False or question_count < 1:
            print("The parameter question_count must be an integer greater than 0.")
            return "Couldn't create the questions for an unknown Quiz."

        for question_number in range(question_count):

            # creates a random number of options, this is just for testing it should generate wathever the user wants
            options_count = random.randint(2, 5)
            correct_option = random.randint(0, options_count-1)
            max_score = quiz_max_score / question_count;

            new_id = self.__get_next_question_id()
            code = quiz.code + "_Q" + "-" + str(question_number)

            new_question = Question(
                id=new_id, uri="-", code=code, text="Choose the right answer.", score=0.0, max_score=max_score,
                option_count=options_count
            )

            self.create_options(new_question, options_count, correct_option)

            quiz.questions.append(new_question)

    '''
        Creates {options_count} number of options to the question passed as parameter
    '''
    def create_options(self, question, options_count, correct_option):

        if isinstance(question, Question) is False:
            print("The parameter quiz is not an instance of Quiz.")
            return "Couldn't create the questions for an unknown Quiz."

        if isinstance(options_count, int) is False or options_count < 2:
            print("The parameter question_count must be an integer greater than 1.")
            return "Couldn't create the questions for an unknown Quiz."

        for option_count in range(options_count):
            new_id = self.__get_next_option_id()
            code = question.code + "_" + 'O' + "-" + str(option_count)

            is_correct = False
            if option_count == correct_option:
                is_correct = True

            new_option = Option(
                id=new_id, uri='-', code=code, text="This is an option!", is_correct=is_correct, is_selected=False, score=0.0
            )
            question.options.append(new_option)


    def __get_next_quiz_id(self):
        self.quiz_id_seq = self.quiz_id_seq + 1
        return self.quiz_id_seq

    def __get_next_question_id(self):
        self.question_id_seq = self.question_id_seq + 1
        return self.question_id_seq

    def __get_next_option_id(self):
        self.option_id_seq = self.option_id_seq + 1
        return self.option_id_seq


