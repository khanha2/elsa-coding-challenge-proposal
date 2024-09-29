from typing import List, Union

from fastapi import FastAPI, HTTPException

from core.domains.quiz import repository as quiz_repository, actions as quiz_actions
from core.domains.quiz.structs import Answer

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
    return quiz


@app.get('/quizzes/{quiz_id}/questions')
def get_quiz_questions(quiz_id: int):
    '''
    Retrive quiz questions by quiz code
    '''
    questions = quiz_repository.list_questions_by_quiz_id(quiz_id)
    return questions


@app.post('/quizzes/{quiz_id}/submit')
def answer_quiz(quiz_id: int, answers: List[Answer]):
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
