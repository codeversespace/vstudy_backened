import re

from fastapi import APIRouter, Request

from app.auth.auth_handler import signJWT
from utilities.response import returnResponse
from utilities import mysql_conn

router = APIRouter()
responseHandler = returnResponse()

@router.post("/generate-token", tags=['Generate Token'])
async def generate_token(request: Request):
    # return token
    body = await request.json()

    reg_id = int(re.search(r'\d+', body['regId']).group())
    password = body['password']
    query = f"SELECT * from users WHERE regId  = '{reg_id}' AND password = '{password}'"
    data = mysql_conn.mysql_obj().mysql_execute(query, fetch_result=True)
    print(data)
    mysql_conn.mysql_obj().close()

    jwt_token = signJWT(reg_id)
    if not data:
        return responseHandler.responseBody(status_code='3001', msg="Invalid Credentials")
    return responseHandler.responseBody(status_code='2001', data=data, jwt  = jwt_token)
    # return payload


@router.post("/user/is-exist")
async def check_if_user_exist(request: Request):
    body = await request.json()
    registration_id = body['reg_id']
    return mysql_conn.mysql_obj().if_exist('users', ['regId'], [registration_id])


# register a user
@router.post("/user")
async def register_user(request: Request):
    data = {}
    body = await request.json()
    query = f"INSERT INTO users (regId,name,class,school,email,phone,password,role) " \
            f"VALUES ({body['regId']},'{body['name']}',{body['class']},{body['school']},'{body['email']}',{body['phone']},'{body['password']}','student')"
    # {"regId": "123", "name": "Syed Abdullah", "class": 1, "school": "09890", "email": "sayedabdullah11@gmail.com",
    #  "phone": 919199191, "password": "123"}
    mysql_conn.mysql_obj().mysql_execute(query, fetch_result=False)
    mysql_conn.mysql_obj().commit()
    if mysql_conn.mysql_obj().mysql_cursor().rowcount < 1:
        data["status"] = "failed to submit answer keys"
        return responseHandler.responseBody(status_code='3015', data=data)
    data["status"] = "Answer sheet submitted"
    return responseHandler.responseBody(status_code='2015', data=data)
