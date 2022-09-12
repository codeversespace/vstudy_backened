# add level
from utilities import mysql_conn
from fastapi import APIRouter, Request

from utilities.response import returnResponse

router = APIRouter()
responseHandler = returnResponse()


@router.post("/add/level")
async def add_subject(request: Request):
    data = {}
    body = await request.json()
    query = f"INSERT INTO level (level_title,level_desc,level_class) VALUES ('{body['title']}','{body['description']}','{body['class']}')"
    m_conn = mysql_conn.mysql_obj()
    m_conn.mysql_execute(query, fetch_result=False)
    m_conn.commit()
    m_conn.close()
    data["status"] = "Level added"
    return responseHandler.responseBody(status_code='2013', data=data)


@router.get("/level")
async def get_level():
    m_conn = mysql_conn.mysql_obj()
    query = f"SELECT * FROM level"
    data = m_conn.mysql_execute(query, fetch_result=True)
    m_conn.close()
    if not data:
        return responseHandler.responseBody(status_code='3014')
    return responseHandler.responseBody(status_code='2014', data=data)
