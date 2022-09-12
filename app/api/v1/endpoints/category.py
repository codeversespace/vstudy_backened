from fastapi import Depends, APIRouter
from fastapi import Request

from app.auth.auth_bearer import JWTBearer
from utilities import mysql_conn
from utilities.response import returnResponse

router = APIRouter()
responseHandler = returnResponse()

@router.get("/category", dependencies=[Depends(JWTBearer())])
async def get_categories():
    query = f"SELECT * from categories"
    m_conn = mysql_conn.mysql_obj()
    data = m_conn.mysql_execute(query, fetch_result=True)
    m_conn.close()
    if not data:
        return responseHandler.responseBody(status_code='3002')
    return responseHandler.responseBody(status_code='2002', data=data)


@router.post("/add/category", dependencies=[Depends(JWTBearer())])
async def add_category(request: Request):
    data = {}
    body = await request.json()
    query = f"INSERT INTO categories (cat_title,cat_desc) VALUES ('{body['title']}','{body['description']}')"
    m_conn = mysql_conn.mysql_obj()
    m_conn.mysql_execute(query, fetch_result=False)
    m_conn.commit()
    if m_conn.mysql_cursor().rowcount < 1:
        data["status"] = "failed to insert"
        return responseHandler.responseBody(status_code='3008', data=data)
    m_conn.close()
    data["status"] = "Category added"
    return responseHandler.responseBody(status_code='2008', data=data)
