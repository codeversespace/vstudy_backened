from fastapi import UploadFile, APIRouter, Depends,Header

from app.api.v1.validator import if_request_valid
from app.auth.auth_bearer import JWTBearer
from app.auth.auth_handler import decodeJWT
from utilities.excel_handler import excel_to_db
from utilities.response import returnResponse

router = APIRouter()
responseHandler = returnResponse()

@router.post("/upload", summary="Register students",
          description="Upload excel file with a fix format asked by admin. This endpoint will "
                      "insert all the data in database in single query.\nNote: Please make sure you are entering valid data in each cells.",
             dependencies=[Depends(JWTBearer())])
async def bulk_register_student(file: UploadFile, Authorization=Header(default=None)):
    if not if_request_valid('super', decodeJWT(Authorization.replace('Bearer ', ''))['user_id']):
        return responseHandler.responseBody(status_code='3999')
    upload_file_path = __upload_excel_return_path(file)
    excel_to_db(upload_file_path, 'users',
                ['regId', 'name', 'class', 'school', 'email', 'phone', 'password', 'role'])
    return


def __upload_excel_return_path(file: UploadFile):
    try:
        contents = file.file.read()
        upload_file_path = f'../../../assets/uploaded-data/{file.filename}'
        with open(upload_file_path, 'wb') as f:
            f.write(contents)
            print(contents)
    except Exception:
        return {"message": "There was an error uploading the file"}
    finally:
        file.file.close()

    return upload_file_path
