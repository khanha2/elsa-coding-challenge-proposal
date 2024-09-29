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


@app.get('/quizzes/{quiz_code}')
def get_quiz(quiz_code: str):
    '''
    Retrive quiz by quiz code
    '''
    quiz = quiz_repository.get_quiz(quiz_code)
    return quiz


# @app.post('/create-session')
# def create_session():
#     return {"Hello": "World"}


# @app.post("/evaluate-answer")
# def evaluate_answer():
#     evaluate_answer()
#     return {"Hello": "World"}


# @app.get("/scoreboard")
# def scoreboard():
#     return {"Hello": "World"}
