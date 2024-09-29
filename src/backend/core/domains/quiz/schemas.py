from typing import List

from pydantic import BaseModel


class Answer(BaseModel):
    question_id: int
    answer: str


class ParticipantResult(BaseModel):
    quiz_id: int
    session_id: str
    user_name: str
    total_score: int
    answers: List[Answer]
