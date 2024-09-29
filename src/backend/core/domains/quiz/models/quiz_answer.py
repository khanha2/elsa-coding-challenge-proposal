
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from core.db.database import Base


class QuizAnswer(Base):
    __tablename__ = 'quiz_answers'

    id = Column(Integer, primary_key=True)
    quiz_participant = relationship('QuizPaticipant')
    answer = Column(String)
    score = Column(Integer, default=0)
