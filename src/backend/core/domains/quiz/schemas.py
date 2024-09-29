from pydantic import BaseModel


class Answer(BaseModel):
    question_id: int
    answer: str
