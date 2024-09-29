from typing import List

from fastapi import FastAPI, HTTPException

from core.domains.quiz import repository as quiz_repository, actions as quiz_actions
from core.domains.quiz.schemas import Answer

from .schemas import QuizSchema, QuizQuestionSchema

app = FastAPI()


@app.get('/')
def index():
    '''
    Return the welcome message
    '''
    return {'message': 'welcome to the quiz app'}


@app.get('/quizzes/{quiz_id}')
def get_quiz(quiz_id: int):
    '''
    Retrive quiz by quiz id
    '''
    quiz = quiz_repository.get_quiz_by_id(quiz_id)
    if not quiz:
        raise HTTPException(status_code=404, detail='not found')
    return QuizSchema.model_validate(quiz)


@app.get('/quizzes/{quiz_id}/questions')
def get_quiz_questions(quiz_id: int):
    '''
    Retrive quiz questions by quiz code
    '''
    questions = [
        QuizQuestionSchema.model_validate(question)
        for question in quiz_repository.list_questions_by_quiz_id(quiz_id)
    ]
    return questions


@app.post('/quizzes/{quiz_id}/submit')
def submit_anwsers(quiz_id: int, answers: List[Answer]):
    '''
    Submit quiz answers
    '''
    quiz = quiz_repository.get_quiz_by_id(quiz_id)
    if not quiz:
        raise HTTPException(status_code=404, detail='not found')
    score = quiz_actions.evaluate_answers(quiz, answers)
    return {'total_score': score}


@app.get('/quizzes/scoreboard')
def get_scoreboard():
    '''
    Retrieve scoreboard
    '''
    return {'message': 'Scoreboard'}
