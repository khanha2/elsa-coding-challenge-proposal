
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSONB

from core.db.database import Base


class QuizPaticipant(Base):
    __tablename__ = 'quiz_participants'

    id = Column(Integer, primary_key=True)
    quiz = relationship('Quiz')
    session_id = Column(String)
    user_name = Column(String)
    total_score = Column(Integer, default=0)
    answers = Column(JSONB, nullable=True)
