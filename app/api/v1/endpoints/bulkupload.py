from fastapi import UploadFile, APIRouter, Depends, Header, Form, File

from app.api.v1.validator import if_request_valid
from app.auth.auth_bearer import JWTBearer
from app.auth.auth_handler import decodeJWT
from app.utilities.excel_handler import excel_to_db, add_questions_from_xl
from app.utilities.response import returnResponse

from pathlib import Path

router = APIRouter()
responseHandler = returnResponse()


@router.post("/upload", summary="Register students",
             description="Upload excel file with a fix format asked by admin. This endpoint will "
                         "insert all the data in database in single query./nNote: Please make sure you are entering valid data in each cells.",
             dependencies=[Depends(JWTBearer())])
async def bulk_register_student(file: UploadFile =File(...), Authorization=Header(default=None)):
    if not if_request_valid('super', decodeJWT(Authorization.replace('Bearer ', ''))['user_id']):
        return responseHandler.responseBody(status_code='3999')
    upload_file_path = __upload_excel_return_path(file)
    excel_to_db(upload_file_path, 'users',
                ['regId', 'name', 'class', 'school', 'email', 'phone', 'password', 'role'])
    return


def __upload_excel_return_path(file, parent_dir_if_any: str = None):
    if parent_dir_if_any == None:
        parent_dir_if_any = ''
    else:
        parent_dir_if_any+='/'
    try:
        contents = file.file.read()
        
        upload_file_path = f'D:/projects/vstudy_backened/app/assets/uploaded-data/{parent_dir_if_any}{file.filename}'
        with open(upload_file_path, 'wb') as f:
            f.write(contents)
    except Exception:
        return {"message": "There was an error uploading the file"}
    finally:
        file.file.close()

    return upload_file_path


@router.post("/add/study-material")
async def submit(file: UploadFile = File(...), class_st=Form(...), subject=Form(...), chapterName=Form(...)):
    upload_data_category = 'study-material'
    dir_path = f'app/assets/uploaded-data/{upload_data_category}/{class_st}/{subject}/{chapterName}'
    Path(dir_path).mkdir(parents=True, exist_ok=True)
    filename = f'{dir_path}/{file.filename}'
    f = open(f'{filename}', 'wb')
    content = await file.read()
    f.write(content)
    return True


@router.post("/add/excel-questions")
def add_questions_from_xl_to_db(file: UploadFile = File(...)):
    excel_path = __upload_excel_return_path(file)
    add_questions_from_xl(excel_path)
    return True

