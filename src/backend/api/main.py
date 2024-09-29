from typing import Union

from fastapi import FastAPI

from core.domains.quiz import repository as quiz_repository

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
    return quiz


@app.get('/quizzes/{quiz_id}/questions')
def get_quiz_questions(quiz_id: int):
    '''
    Retrive quiz questions by quiz code
    '''
    questions = quiz_repository.list_questions_by_quiz_id(quiz_id)
    return questions


@app.post('/quizzes/{quiz_id}/submit')
def answer_quiz(quiz_id: int):
    '''
    Submit quiz answers
    '''
    quiz = quiz_repository.get_quiz_by_id(quiz_id)
    return quiz


@app.get('/quizzes/scoreboard')
def get_scoreboard():
    '''
    Retrieve scoreboard
    '''
    return {'message': 'Scoreboard'}
