# add subject
from fastapi import Request, APIRouter

from utilities import mysql_conn
from utilities.response import returnResponse

router = APIRouter()
responseHandler = returnResponse()


@router.post("/add/subject")
async def add_subject(request: Request):
    data = {}
    body = await request.json()
    query = f"INSERT INTO subject (sub_title,sub_desc) VALUES ('{body['title']}','{body['description']}')"
    m_conn = mysql_conn.mysql_obj()
    m_conn.mysql_execute(query, fetch_result=False)
    m_conn.commit()
    m_conn.close()
    # if mysql_conn.mysql_obj().mysql_cursor().rowcount < 1:
    #     data["status"] = "failed to add subject"
    #     return responseHandler.responseBody(status_code='3011', data=data)
    data["status"] = "Subject added"
    return responseHandler.responseBody(status_code='2011', data=data)


@router.get("/subject")
async def get_subject():
    m_conn =mysql_conn.mysql_obj()
    query = f"SELECT * FROM subject"
    data = m_conn.mysql_execute(query, fetch_result=True)
    m_conn.close()
    if not data:
        return responseHandler.responseBody(status_code='3012')
    return responseHandler.responseBody(status_code='2012', data=data)
