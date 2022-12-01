# get all questions of a given category
from fastapi import APIRouter, Request, Depends, Header

from app.api.v1.validator import if_request_valid
from app.auth.auth_bearer import JWTBearer
from app.auth.auth_handler import decodeJWT
from app.utilities import mysql_conn
from app.utilities.response import returnResponse

router = APIRouter()
responseHandler = returnResponse()


@router.get("/category/questions/{cat_id}", dependencies=[Depends(JWTBearer())])
async def get_questions_from_category(cat_id: str):
    query = f"SELECT * FROM mcqs INNER JOIN quiz ON quiz.q_id = mcqs.q_id where quiz.cat_id = {cat_id};"
    m_conn = mysql_conn.mysql_obj()
    data = m_conn.mysql_execute(query, fetch_result=True)
    m_conn.close()
    if not data:
        return responseHandler.responseBody(status_code='3006')
    return responseHandler.responseBody(status_code='2006', data=data)


# get all questions of a given quiz
@router.get("/question/quiz/{quiz_id}", dependencies=[Depends(JWTBearer())])
async def get_questions_from_quiz_id(quiz_id: str):
    m_conn = mysql_conn.mysql_obj()
    query = f"SELECT question_list from quiz where q_id = {quiz_id}"
    ques_id_list = m_conn.mysql_execute(query, fetch_result=True)[0]['question_list']
    ques_id_str = str(ques_id_list)[1:-1]
    print(ques_id_str)
    query = f"SELECT q_id,ques_id,content,opt1,opt2,opt3,opt4 FROM mcqs where ques_id in ({ques_id_str});"
    data = m_conn.mysql_execute(query, fetch_result=True)
    m_conn.close()
    if not data:
        return responseHandler.responseBody(status_code='3007')
    return responseHandler.responseBody(status_code='2007', data=data)


@router.get("/question/quiz/all/{quiz_id}", dependencies=[Depends(JWTBearer())])
async def get_questions_from_quiz_id(quiz_id: str):
    m_conn = mysql_conn.mysql_obj()
    query = f"SELECT * FROM mcqs where q_id = {quiz_id};"
    data = m_conn.mysql_execute(query, fetch_result=True)
    m_conn.close()
    if not data:
        return responseHandler.responseBody(status_code='3007')
    return responseHandler.responseBody(status_code='2007', data=data)


@router.post("/add/question", dependencies=[Depends(JWTBearer())])
async def add_question(request: Request, Authorization=Header(default=None)):
    if not if_request_valid('super', decodeJWT(Authorization.replace('Bearer ', ''))['user_id']):
        return responseHandler.responseBody(status_code='3999')
    data = {}
    m_conn = mysql_conn.mysql_obj()
    body = await request.json()
    # will get added by value from UI
    query = f"INSERT INTO mcqs (q_id,content,opt1,opt2,opt3,opt4,ans,added_by,sub_id,class) VALUES ('{body['q_id']}','{body['content']}'," \
            f"'{body['option1']}','{body['option2']}','{body['option3']}','{body['option4']}','{body['answer']}','{body['added_by']}',{body['sub_id']},{body['class']})"
    m_conn.mysql_execute(query, fetch_result=False)
    m_conn.commit()
    m_conn.close()
    data["status"] = "question added"
    return responseHandler.responseBody(status_code='2008', data=data)

