import time

from fastapi import APIRouter, Request

from utilities import mysql_conn
from utilities.response import returnResponse

router = APIRouter()
responseHandler = returnResponse()

@router.get("/quiz")
async def get_categories():
    query = f"SELECT * FROM quiz INNER JOIN categories ON categories.cat_id=quiz.cat_id"
    m_conn = mysql_conn.mysql_obj()
    data = m_conn.mysql_execute(query, fetch_result=True)
    m_conn.close()
    if not data:
        return responseHandler.responseBody(status_code='3003')
    return responseHandler.responseBody(status_code='2003', data=data)


@router.get("/quiz/active/{stu_id}")
async def get_categories(stu_id:str =None):
    m_conn =  mysql_conn.mysql_obj()
    query = f"SELECT * FROM quiz INNER JOIN categories ON categories.cat_id=quiz.cat_id WHERE quiz.active=1"
    data = m_conn.mysql_execute(query, fetch_result=True)
    for i  in range(len(data)):
        query_ = f"select ans_keys from ans_sheet where student_id = {stu_id} and q_id = {data[i]['q_id']} and ans_keys IS NOT NULL"
        data_ = m_conn.mysql_execute(query_, fetch_result=True)
        quiz_submitted_by_user = False
        if data_:
            if  len(data_[0]['ans_keys']) > 4 :
                quiz_submitted_by_user = True
        data[i]['quiz_submitted_by_user'] = quiz_submitted_by_user
    m_conn.close()
    if not data:
        return responseHandler.responseBody(status_code='3004')
    return responseHandler.responseBody(status_code='2004', data=data)


# http://localhost:8000/quiz/category/active/1
@router.get("/quiz/category/active/{cat_id}")
async def get_category(cat_id: str):
    m_conn = mysql_conn.mysql_obj()
    query = f"SELECT * FROM quiz INNER JOIN categories ON categories.cat_id=quiz.cat_id WHERE quiz.active=1 AND quiz.cat_id={cat_id}"
    data = m_conn.mysql_execute(query, fetch_result=True)
    m_conn.close()
    if not data:
        return responseHandler.responseBody(status_code='3005')
    return responseHandler.responseBody(status_code='2005', data=data)

@router.get("/quiz/{id}")
async def get_quiz_detail(id: str):
    m_conn = mysql_conn.mysql_obj()
    query = f"SELECT * FROM quiz WHERE q_id = {id}"
    data = m_conn.mysql_execute(query, fetch_result=True)
    m_conn.close()
    if not data:
        return responseHandler.responseBody(status_code='3003')
    return responseHandler.responseBody(status_code='2003', data=data)

@router.post("/add/quiz")
async def add_quiz(request: Request):
    data = {}
    m_conn = mysql_conn.mysql_obj()
    body = await request.json()
    query = f"INSERT INTO quiz (title,description,max_marks,no_of_ques,active,cat_id,level_id,time_per_qstn_ms) VALUES ('{body['title']}','{body['description']}'," \
            f"'{body['maxMarks']}','{body['numberOfQuestions']}',{body['active']},'{body['cat_id']}','{body['level_id']}','60000')"
    m_conn.mysql_execute(query, fetch_result=False)
    m_conn.commit()
    if m_conn.mysql_cursor().rowcount < 1:
        data["status"] = "failed to insert quiz"
        return responseHandler.responseBody(status_code='3008', data=data)
    m_conn.close()
    data["status"] = "Quiz added"
    return responseHandler.responseBody(status_code='2008', data=data)


@router.post("/ans/get-quiz-start-time")
async def get_quiz_start_time_and(request: Request):
    body = await request.json()
    q_id = body['q_id']
    stu_id = body['stu_id']
    m_conn = mysql_conn.mysql_obj()
    query = f"SELECT quiz.time_per_qstn_ms, ans_sheet.started_at FROM quiz RIGHT JOIN ans_sheet ON quiz.q_id=ans_sheet.q_id WHERE ans_sheet.student_id = {stu_id} AND ans_sheet.q_id ={q_id}"
    data = m_conn.mysql_execute(query, fetch_result=True)
    if not data:
        # insert quiz startup data
        curr_time_ms = int(time.time() * 1000.0)
        query = f"INSERT INTO ans_sheet (student_id,q_id,started_at) VALUES ({stu_id},{q_id},{curr_time_ms})"
        m_conn.mysql_execute(query, fetch_result=False)
        m_conn.commit()
        query = f"SELECT quiz.time_per_qstn_ms, ans_sheet.started_at FROM quiz RIGHT JOIN ans_sheet ON quiz.q_id=ans_sheet.q_id WHERE ans_sheet.student_id = {stu_id} AND ans_sheet.q_id ={q_id}"
        data = m_conn.mysql_execute(query, fetch_result=True)
    m_conn.close()
    return responseHandler.responseBody(status_code='2003', data=data)


