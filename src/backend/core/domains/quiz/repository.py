from sqlalchemy import select


from core.db import database

from .models import Quiz


async def get_quiz(quiz_code: str) -> Quiz:
    '''
    Retrieve quiz by quiz code
    '''
    query = select(Quiz).where(Quiz.code == quiz_code)
    session = database.retrieve_db_session()
    result = await session.execute(query)
    return result.first()
