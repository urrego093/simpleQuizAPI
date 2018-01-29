from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, Text, FLOAT, ForeignKey, BOOLEAN
from sqlalchemy.orm import relationship

Base = declarative_base()


def get_next_id():
    return Quiz.id_seq


class Quiz(Base):
    __tablename__ = 'quiz'

    id = Column(Integer, primary_key=True)
    uri = Column(Text, nullable=False)
    code = Column(Text, nullable=False)
    name = Column(Text, nullable=False)
    description = Column(Text, nullable=False)
    score = Column(FLOAT, nullable=False)
    max_score = Column(FLOAT, nullable=False)
    question_count = Column(Integer, nullable=False)
    questions = relationship("Question", back_populates="quiz")

    def __repr__(self):
        return "[{}] Name: {}, Score:{}, Question_count: {}, URI: {}".format(self.code, self.name, self.score, self.question_count, self.uri)

class Question(Base):
    __tablename__ = 'question'

    id = Column(Integer, primary_key=True)
    uri = Column(Text, nullable=False)
    code = Column(Text, nullable=False)
    text = Column(Text, nullable=False)
    score = Column(FLOAT, nullable=False)
    max_score = Column(FLOAT, nullable=False)
    option_count = Column(Integer, nullable=False)
    quiz_id = Column(Integer, ForeignKey('quiz.id'))
    quiz = relationship("Quiz", back_populates="questions")

    options = relationship("Option", back_populates="question")

    def __repr__(self):
        return "[{}] {}, Score: {} Max_score: {}, URI: {}, Option Count: {}".format(self.code, self.text, self.score, self.max_score, self.uri, self.option_count)


class Option(Base):
    __tablename__ = 'option'

    id = Column(Integer, primary_key=True)
    uri = Column(Text, nullable=False)
    code = Column(Text, nullable=False)
    text = Column(Text, nullable=False)
    score = Column(FLOAT, nullable=False)
    is_correct = Column(BOOLEAN, nullable=False)
    is_selected = Column(BOOLEAN, nullable=False)

    question_id = Column(Integer, ForeignKey('question.id'))
    question = relationship("Question", back_populates="options")

    def __repr__(self):
        return "[{}] {}, Score: {} Is correct: {}, URI: {}".format(
            self.code, self.text, self.score, self.is_correct, self.uri
        )
