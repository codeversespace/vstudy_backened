# add subject
from fastapi import Request, APIRouter, Depends, Header

from app.api.v1.validator import if_request_valid
from app.auth.auth_bearer import JWTBearer
from app.auth.auth_handler import decodeJWT
from app.utilities import mysql_conn
from app.utilities.response import returnResponse
from app.utilities.vstd_utils import getCode

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


@router.get("/study-material/get-subject-list/{_class}")
async def get_subject(_class):
    m_conn = mysql_conn.mysql_obj()
    query = f"SELECT distinct subject_code FROM study_material WHERE class = {_class}"
    data = m_conn.mysql_execute(query, fetch_result=True)
    m_conn.close()
    subjectList = []
    for i in data:
        subjectList.append(getCode.subjectById(i['subject_code']))
    
    return subjectList

# get study-material path list inputs: subject and class
@router.get("/study-material/get-chapter-list/{_class}/{subject}")
async def get_chapter_list(_class,subject):
    sub_code = getCode.subject(subject)
    m_conn = mysql_conn.mysql_obj()
    query = f"SELECT file_path, chapter_name FROM study_material WHERE class = {_class} and subject_code = {sub_code}"
    data = m_conn.mysql_execute(query, fetch_result=True)
    m_conn.close()
    return_data = {}
    for i in data:
        file_path = f"{_class}/{subject}/{i['file_path']}"
        return_data[i['chapter_name']] = file_path
    return return_data
