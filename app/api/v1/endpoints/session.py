import time

from fastapi import APIRouter, Request, Depends,Header

from app.api.v1.validator import if_request_valid
from app.auth.auth_bearer import JWTBearer
from app.auth.auth_handler import decodeJWT
from app.utilities import mysql_conn
from app.utilities.response import returnResponse

router = APIRouter()
responseHandler = returnResponse()

@router.get("/session/if-valid",dependencies=[Depends(JWTBearer())])
def session_valid():
    return

