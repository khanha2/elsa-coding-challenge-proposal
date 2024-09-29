from typing import List

from core.db import database

from .models import Quiz, QuizQuestion


def get_quiz_by_id(quiz_id: int) -> Quiz:
    '''
    Retrieve quiz by quiz code
    '''
    session = database.retrieve_db_session()
    return session.query(Quiz).filter(Quiz.id == quiz_id).first()


def list_questions_by_quiz_id(quiz_id: int) -> List[QuizQuestion]:
    '''
    Retrieve questions by quiz id
    '''
    session = database.retrieve_db_session()
    return session.query(QuizQuestion).filter(QuizQuestion.quiz_id == quiz_id).all()
