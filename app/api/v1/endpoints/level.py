# add level
from app.api.v1.validator import  if_request_valid
from app.auth.auth_bearer import JWTBearer
from app.auth.auth_handler import decodeJWT
from app.utilities import mysql_conn
from fastapi import APIRouter, Request, Depends,Header

from app.utilities.response import returnResponse

router = APIRouter()
responseHandler = returnResponse()


@router.post("/add/level",dependencies=[Depends(JWTBearer())])
async def add_subject(request: Request, Authorization=Header(default=None)):
    if not if_request_valid('super', decodeJWT(Authorization.replace('Bearer ', ''))['user_id']):
        return responseHandler.responseBody(status_code='3999')
    data = {}
    body = await request.json()
    query = f"INSERT INTO level (level_title,level_desc,level_class) VALUES ('{body['title']}','{body['description']}','{body['class']}')"
    m_conn = mysql_conn.mysql_obj()
    m_conn.mysql_execute(query, fetch_result=False)
    m_conn.commit()
    
    data["status"] = "Level added"
    return responseHandler.responseBody(status_code='2013', data=data)


@router.get("/level",dependencies=[Depends(JWTBearer())])
async def get_level():
    m_conn = mysql_conn.mysql_obj()
    query = f"SELECT * FROM level"
    data = m_conn.mysql_execute(query, fetch_result=True)
    
    if not data:
        return responseHandler.responseBody(status_code='3014')
    return responseHandler.responseBody(status_code='2014', data=data)
