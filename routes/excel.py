from fastapi import FastAPI, UploadFile, APIRouter

from utilities.excel_handler import excel_to_db

router_contacts = APIRouter(
    prefix="/action/bulk",
    tags=["Bulk action upload, delete, update etc"]
)

bulk_upload = FastAPI()


@bulk_upload.post("/upload", summary="Register students",
          description="Upload excel file with a fix format asked by admin. This endpoint will "
                      "insert all the data in database in single query.\nNote: Please make sure you are entering valid data in each cells.")
async def bulk_register_student(file: UploadFile):
    upload_file_path = upload_excel_return_path(file)
    excel_to_db(upload_file_path, 'users',
                ['regId', 'name', 'class', 'school', 'email', 'phone', 'password', 'role'])


async def upload_excel_return_path(file: UploadFile):
    try:
        contents = file.file.read()
        upload_file_path = f'assets/uploaded-data/{file.filename}'
        with open(upload_file_path, 'wb') as f:
            f.write(contents)
    except Exception:
        return {"message": "There was an error uploading the file"}
    finally:
        file.file.close()

    return {"message": f"Successfully uploaded {upload_file_path}"}
