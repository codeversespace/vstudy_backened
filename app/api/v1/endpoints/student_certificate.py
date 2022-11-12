from fastapi import APIRouter

from app.utilities import mysql_conn
from app.utilities.response import returnResponse

router = APIRouter()
responseHandler = returnResponse()


@router.get("/certificate/{student_id}/{cert_id}")
def get_certificate_details(cert_id: int = None, student_id: int = None):
    query = f"SELECT student_certificate.id,student_certificate.quiz_id, users.name from " \
            f"student_certificate join users on student_certificate.student_id = users.regId where users.regId = {student_id} and student_certificate.id = {cert_id};"
    m_conn = mysql_conn.mysql_obj()
    data = m_conn.mysql_execute(query, fetch_result=True)
    m_conn.close()
    if not data:
        return responseHandler.responseBody(status_code='3020')
    return responseHandler.responseBody(status_code='2020', data=data)

