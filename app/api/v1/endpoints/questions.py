# get all questions of a given category
from fastapi import APIRouter, Request

from utilities import mysql_conn
from utilities.response import returnResponse

router = APIRouter()
responseHandler = returnResponse()


@router.get("/category/questions/{cat_id}")
async def get_questions_from_category(cat_id: str):
    query = f"SELECT * FROM mcqs INNER JOIN quiz ON quiz.q_id = mcqs.q_id where quiz.cat_id = {cat_id};"
    data = mysql_conn.mysql_obj().mysql_execute(query, fetch_result=True)
    if not data:
        return responseHandler.responseBody(status_code='3006')
    return responseHandler.responseBody(status_code='2006', data=data)


# get all questions of a given quiz
@router.get("/question/quiz/{quiz_id}")
async def get_questions_from_quiz_id(quiz_id: str):
    m_conn = mysql_conn.mysql_obj()
    query = f"SELECT q_id,ques_id,content,opt1,opt2,opt3,opt4 FROM mcqs where q_id = {quiz_id};"
    data = m_conn.mysql_execute(query, fetch_result=True)
    if not data:
        return responseHandler.responseBody(status_code='3007')
    return responseHandler.responseBody(status_code='2007', data=data)


@router.get("/question/quiz/all/{quiz_id}")
async def get_questions_from_quiz_id(quiz_id: str):
    m_conn = mysql_conn.mysql_obj()
    query = f"SELECT * FROM mcqs where q_id = {quiz_id};"
    data = m_conn.mysql_execute(query, fetch_result=True)
    if not data:
        return responseHandler.responseBody(status_code='3007')
    return responseHandler.responseBody(status_code='2007', data=data)


@router.post("/add/question")
async def add_quiz(request: Request):
    data = {}
    m_conn =  mysql_conn.mysql_obj()
    body = await request.json()
    # will get added by value from UI
    query = f"INSERT INTO mcqs (q_id,content,opt1,opt2,opt3,opt4,ans,added_by,sub_id,class) VALUES ('{body['q_id']}','{body['content']}'," \
            f"'{body['option1']}','{body['option2']}','{body['option3']}','{body['option4']}','{body['answer']}','{body['added_by']}',{body['sub_id']},{body['class']})"
    m_conn.mysql_execute(query, fetch_result=False)
    m_conn.commit()
    if m_conn.mysql_cursor().rowcount < 1:
        data["status"] = "failed to add question"
        return responseHandler.responseBody(status_code='3008', data=data)
    data["status"] = "question added"
    return responseHandler.responseBody(status_code='2008', data=data)
