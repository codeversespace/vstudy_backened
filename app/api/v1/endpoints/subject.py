# add subject
from fastapi import Request, APIRouter, Depends, Header

from app.api.v1.validator import if_request_valid
from app.auth.auth_bearer import JWTBearer
from app.auth.auth_handler import decodeJWT
from utilities import mysql_conn
from utilities.response import returnResponse

router = APIRouter()
responseHandler = returnResponse()


@router.post("/add/subject", dependencies=[Depends(JWTBearer())])
async def add_subject(request: Request, Authorization=Header(default=None)):
    if not if_request_valid('super', decodeJWT(Authorization.replace('Bearer ', ''))['user_id']):
        return responseHandler.responseBody(status_code='3999')
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


@router.get("/subject", dependencies=[Depends(JWTBearer())])
async def get_subject():
    m_conn = mysql_conn.mysql_obj()
    query = f"SELECT * FROM subject"
    data = m_conn.mysql_execute(query, fetch_result=True)
    m_conn.close()
    if not data:
        return responseHandler.responseBody(status_code='3012')
    return responseHandler.responseBody(status_code='2012', data=data)
