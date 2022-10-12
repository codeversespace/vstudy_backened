from fastapi import Depends, APIRouter, Header
from fastapi import Request

from app.api.v1.validator import  if_request_valid
from app.auth.auth_bearer import JWTBearer
from app.auth.auth_handler import decodeJWT
from app.utilities import mysql_conn
from app.utilities.response import returnResponse

router = APIRouter()
responseHandler = returnResponse()
# def __if_request_valid(role_level,user_id):
#     if role_level.lower() == 'super':
#         if user_id in RoleAuthenticator.SuperRole.role_list:
#             return True



@router.get("/category", dependencies=[Depends(JWTBearer())])
async def get_categories():
    query = f"SELECT * from categories"
    m_conn = mysql_conn.mysql_obj()
    data = m_conn.mysql_execute(query, fetch_result=True)
    
    if not data:
        return responseHandler.responseBody(status_code='3002')
    return responseHandler.responseBody(status_code='2002', data=data)


@router.post("/add/category", dependencies=[Depends(JWTBearer())])
async def add_category(request: Request,Authorization = Header(default=None)):
    if not if_request_valid('super', decodeJWT(Authorization.replace('Bearer ', ''))['user_id']):
        return responseHandler.responseBody(status_code='3999')
    data = {}
    body = await request.json()
    query = f"INSERT INTO categories (cat_title,cat_desc) VALUES ('{body['title']}','{body['description']}')"
    m_conn = mysql_conn.mysql_obj()
    m_conn.mysql_execute(query, fetch_result=False)
    m_conn.commit()
    if m_conn.mysql_cursor().rowcount < 1:
        data["status"] = "failed to insert"
        return responseHandler.responseBody(status_code='3008', data=data)
    
    data["status"] = "Category added"
    return responseHandler.responseBody(status_code='2008', data=data)
