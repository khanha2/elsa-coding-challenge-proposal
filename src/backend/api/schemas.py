from typing import List
from pydantic import BaseModel, ConfigDict


class QuizQuestionOptionSchema(BaseModel):
    code: str
    content: str


class QuizQuestionSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    content: str
    options: List[QuizQuestionOptionSchema]


class QuizSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    code: str
    name: str
