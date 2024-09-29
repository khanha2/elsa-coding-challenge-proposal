from sqlalchemy import select


from core.db import database

from .models import Quiz


def get_quiz(quiz_code: str) -> Quiz:
    '''
    Retrieve quiz by quiz code
    '''
    session = database.retrieve_db_session()
    return session.query(Quiz).filter(Quiz.code == quiz_code).first()
