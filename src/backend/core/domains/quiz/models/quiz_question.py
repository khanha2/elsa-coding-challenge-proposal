from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship

from core.db.database import Base


class QuizQuestion(Base):
    __tablename__ = 'quiz_questions'

    id = Column(Integer, primary_key=True)
    content = Column(String)
    quiz_id = ForeignKey('Quiz.id')
    score = Column(Integer, default=1)
    expected_option = Column(String, nullable=True)
    # Structure of options: [{'code': 'A', 'content': 'content of option A'}, ...]
    options = Column(JSONB, nullable=True)
