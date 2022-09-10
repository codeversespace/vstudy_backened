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
    mysql_conn.mysql_obj().mysql_execute(query, fetch_result=False)
    mysql_conn.mysql_obj().commit()
    if mysql_conn.mysql_obj().mysql_cursor().rowcount < 1:
        data["status"] = "failed to add subject"
        return responseHandler.responseBody(status_code='3011', data=data)
    data["status"] = "Subject added"
    return responseHandler.responseBody(status_code='2011', data=data)


@router.get("/subject")
async def get_subject():
    query = f"SELECT * FROM subject"
    data = mysql_conn.mysql_obj().mysql_execute(query, fetch_result=True)
    if not data:
        return responseHandler.responseBody(status_code='3012')
    return responseHandler.responseBody(status_code='2012', data=data)
