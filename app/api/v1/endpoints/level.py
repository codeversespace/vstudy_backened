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
    print(query)
    mysql_conn.mysql_obj().mysql_execute(query, fetch_result=False)
    mysql_conn.mysql_obj().commit()
    if mysql_conn.mysql_obj().mysql_cursor().rowcount < 1:
        data["status"] = "failed to add level"
        return responseHandler.responseBody(status_code='3013', data=data)
    data["status"] = "Level added"
    return responseHandler.responseBody(status_code='2013', data=data)


@router.get("/level")
async def get_level():
    query = f"SELECT * FROM level"
    data = mysql_conn.mysql_obj().mysql_execute(query, fetch_result=True)
    if not data:
        return responseHandler.responseBody(status_code='3014')
    return responseHandler.responseBody(status_code='2014', data=data)
