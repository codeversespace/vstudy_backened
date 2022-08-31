from fastapi import FastAPI
from fastapi import Request
from fastapi.middleware.cors import CORSMiddleware
from utilities import mysql_conn
from fastapi.encoders import jsonable_encoder
import re

from utilities.response import returnResponse

responseHandler = returnResponse()
mysql_handler = mysql_conn.mysql_obj()

app = FastAPI()
origins = ["http://localhost:4200"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# add to stock

@app.post("/generate-token")
async def generate_token(request: Request):
    body = await request.json()
    reg_id = int(re.search(r'\d+', body['regId']).group())
    password = body['password']
    query = f"SELECT * from users WHERE regId  = '{reg_id}' AND password = '{password}'"
    data = mysql_handler.mysql_execute(query, fetch_result=True)
    if not data:
        return responseHandler.responseBody(status_code='3001', msg="Invalid Credentials")
    return responseHandler.responseBody(status_code='2001', data=data)
    # return payload

@app.get("/category")
async def get_categories():
    query = f"SELECT * from categories"
    data = mysql_handler.mysql_execute(query, fetch_result=True)
    if not data:
        return responseHandler.responseBody(status_code='3002')
    return responseHandler.responseBody(status_code='2002', data=data)


@app.get("/quiz")
async def get_categories():
    query = f"SELECT * FROM quiz INNER JOIN categories ON categories.cat_id=quiz.cat_id"
    data = mysql_handler.mysql_execute(query, fetch_result=True)
    if not data:
        return responseHandler.responseBody(status_code='3003')
    return responseHandler.responseBody(status_code='2003', data=data)


@app.get("/quiz/active")
async def get_categories():
    query = f"SELECT * FROM quiz INNER JOIN categories ON categories.cat_id=quiz.cat_id WHERE quiz.active=1"
    data = mysql_handler.mysql_execute(query, fetch_result=True)
    if not data:
        return responseHandler.responseBody(status_code='3004')
    return responseHandler.responseBody(status_code='2004', data=data)


# http://localhost:8000/quiz/category/active/1
@app.get("/quiz/category/active/{cat_id}")
async def get_category(cat_id: str):
    query = f"SELECT * FROM quiz INNER JOIN categories ON categories.cat_id=quiz.cat_id WHERE quiz.active=1 AND quiz.cat_id={cat_id}"
    data = mysql_handler.mysql_execute(query, fetch_result=True)
    if not data:
        return responseHandler.responseBody(status_code='3005')
    return responseHandler.responseBody(status_code='2005', data=data)


# get all questions of a given category
@app.get("/category/questions/{cat_id}")
async def get_questions_from_category(cat_id: str):
    query = f"SELECT * FROM mcqs INNER JOIN quiz ON quiz.q_id = mcqs.q_id where quiz.cat_id = {cat_id};"
    data = mysql_handler.mysql_execute(query, fetch_result=True)
    if not data:
        return responseHandler.responseBody(status_code='3006')
    return responseHandler.responseBody(status_code='2006', data=data)


# get all questions of a given quiz
@app.get("/question/quiz/{quiz_id}")
async def get_questions_from_quiz_id(quiz_id: str):
    query = f"SELECT q_id,ques_id,content,opt1,opt2,opt3,opt4 FROM mcqs where q_id = {quiz_id};"
    data = mysql_handler.mysql_execute(query, fetch_result=True)
    if not data:
        return responseHandler.responseBody(status_code='3007')
    return responseHandler.responseBody(status_code='2007', data=data)

@app.get("/question/quiz/all/{quiz_id}")
async def get_questions_from_quiz_id(quiz_id: str):
    query = f"SELECT * FROM mcqs where q_id = {quiz_id};"
    data = mysql_handler.mysql_execute(query, fetch_result=True)
    if not data:
        return responseHandler.responseBody(status_code='3007')
    return responseHandler.responseBody(status_code='2007', data=data)


@app.get("/quiz/{id}")
async def get_quiz_detail(id: str):
    query = f"SELECT * FROM quiz WHERE q_id = {id}"
    data = mysql_handler.mysql_execute(query, fetch_result=True)
    if not data:
        return responseHandler.responseBody(status_code='3003')
    return responseHandler.responseBody(status_code='2003', data=data)


##########
# INSERT #
##########
@app.post("/add/category")
async def add_category(request: Request):
    data = {}
    body = await request.json()
    query = f"INSERT INTO categories (cat_title,cat_desc) VALUES ('{body['title']}','{body['description']}')"
    mysql_handler.mysql_execute(query, fetch_result=False)
    mysql_handler.commit()
    if mysql_handler.mysql_cursor().rowcount < 1:
        data["status"] = "failed to insert"
        return responseHandler.responseBody(status_code='3008', data=data)
    data["status"] = "Category added"
    return responseHandler.responseBody(status_code='2008', data=data)


# if __name__ == "__main__":
#     uvicorn.run(app, host="127.0.0.1", port=5049)

@app.post("/add/quiz")
async def add_quiz(request: Request):
    data = {}
    body = await request.json()
    query = f"INSERT INTO quiz (title,description,max_marks,no_of_ques,active,cat_id) VALUES ('{body['title']}','{body['description']}'," \
            f"'{body['maxMarks']}','{body['numberOfQuestions']}',{body['active']},'{body['cat_id']}')"
    print(query)
    mysql_handler.mysql_execute(query, fetch_result=False)
    mysql_handler.commit()
    if mysql_handler.mysql_cursor().rowcount < 1:
        data["status"] = "failed to insert quiz"
        return responseHandler.responseBody(status_code='3008', data=data)
    data["status"] = "Quiz added"
    return responseHandler.responseBody(status_code='2008', data=data)

@app.post("/add/question")
async def add_quiz(request: Request):
    data = {}
    body = await request.json()
    # will get added by value from UI
    query = f"INSERT INTO mcqs (q_id,content,opt1,opt2,opt3,opt4,ans,added_by) VALUES ('{body['q_id']}','{body['content']}'," \
            f"'{body['option1']}','{body['option2']}','{body['option3']}','{body['option4']}','{body['answer']}','{body['added_by']}')"
    print(query)
    mysql_handler.mysql_execute(query, fetch_result=False)
    mysql_handler.commit()
    if mysql_handler.mysql_cursor().rowcount < 1:
        data["status"] = "failed to add question"
        return responseHandler.responseBody(status_code='3008', data=data)
    data["status"] = "question added"
    return responseHandler.responseBody(status_code='2008', data=data)

#get questions from quiz id