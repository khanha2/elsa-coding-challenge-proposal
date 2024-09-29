
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from core.db.database import Base

class QuizPaticipant(Base):
    __tablename__ = 'quiz_participants'

    id = Column(Integer, primary_key=True)
    quiz = relationship('Quiz')
    session_id = Column(String)
    total_score = Column(Integer, default=0)
