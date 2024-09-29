from typing import List

from ..models import Quiz
from ..repository import list_questions_by_quiz_id
from ..schemas import Answer


def perform(quiz: Quiz, answers: List[Answer]) -> int:
    '''
    Evaluate participant answers
    '''
    question_map = {
        question.id: question for question in list_questions_by_quiz_id(quiz.id)
    }
    total_score = 0
    for answer in answers:
        print(answer)

        question = question_map.get(answer.question_id)
        if not question:
            continue

        if question.expected_option == answer.answer:
            total_score += question.score

    return total_score
