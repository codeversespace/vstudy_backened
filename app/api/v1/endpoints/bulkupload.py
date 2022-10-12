from io import BytesIO

from fastapi import UploadFile, APIRouter, Depends, Header, Form, File, Request

from app.api.v1.validator import if_request_valid
from app.auth.auth_bearer import JWTBearer
from app.auth.auth_handler import decodeJWT
from app.utilities import mysql_conn
from app.utilities.excel_handler import excel_to_db, add_questions_from_xl
from app.utilities.response import returnResponse

from pathlib import Path

from app.utilities.vstd_utils import getCode

router = APIRouter()
responseHandler = returnResponse()


@router.post("/upload", summary="Register students",
             description="Upload excel file with a fix format asked by admin. This endpoint will "
                         "insert all the data in database in single query./nNote: Please make sure you are entering valid data in each cells.",
             dependencies=[Depends(JWTBearer())])
async def bulk_register_student(file: UploadFile = File(...), Authorization=Header(default=None)):
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
        parent_dir_if_any += '/'
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


#it uploads to backend serve
# @router.post("/add/study-material")
# async def submit(file: UploadFile = File(...), class_st=Form(...), subject=Form(...), chapterName=Form(...)):
#     upload_data_category = 'study-material'
#     dir_path = f'app/assets/uploaded-data/{upload_data_category}/{class_st}/{subject}/{chapterName}'
#     Path(dir_path).mkdir(parents=True, exist_ok=True)
#     filename = f'{dir_path}/{file.filename}'
#     f = open(f'{filename}', 'wb')
#     content = await file.read()
#     f.write(content)
#     return True



def upload_ftp(server_addr, ftp_user, ftp_user_pass, dir_path,file,filename):
    from ftplib import FTP
    fileto = BytesIO()
    fileto.write(file)
    fileto.seek(0)
    with FTP(server_addr, ftp_user, ftp_user_pass) as ftp:
        chdir(dir_path, ftp)
        ftp.storbinary(f'STOR {filename}', fileto)

@router.post("/add/study-material")
async def submit(file: UploadFile = File(...), class_st=Form(...), subject=Form(...), chapterName=Form(...)):
    dir_path = f'{class_st}/{subject}/'
    content = await file.read()
    file_name = file.filename
    subject_code = getCode.subject(subject)
    upload_ftp('vstudy.in', 'vstudy-ftp', 'Vstudy@admin@123',dir_path,content, file_name)
    # add filepath data to db
    query = f"INSERT INTO study_material (subject_code,class,file_path,chapter_name) VALUES ({subject_code},{class_st},'{file_name}','{chapterName}')"
    m_conn = mysql_conn.mysql_obj()
    m_conn.mysql_execute(query, fetch_result=False)
    m_conn.commit()
    
    return True

@router.post("/add/excel-questions")
def add_questions_from_xl_to_db(file: UploadFile = File(...)):
    excel_path = __upload_excel_return_path(file)
    add_questions_from_xl(excel_path)
    return True


@router.post("/question/set-question-profile")
async def create_question_profile(request: Request, Authorization=Header(default=None)):
    data = {}
    body = await request.json()
    query = f"INSERT INTO question_set_profile (description,title,weightage_list) VALUES ('{body['name']}','{body['description']}',\"{body['subjectWeightage']}\")"
    print(query)
    m_conn = mysql_conn.mysql_obj()
    m_conn.mysql_execute(query, fetch_result=False)
    m_conn.commit()
    # if m_conn.mysql_cursor().rowcount < 1:
    #     data["status"] = "failed to insert"
    #     return responseHandler.responseBody(status_code='3008', data=data)
    
    data["status"] = "Question set added"
    return responseHandler.responseBody(status_code='2008', data=data)

def convert_to_int_float(n):
    return n
    try:
        return int(n)
    except ValueError:
        return int(n)

def calculate_percentage_value(p_value, total):
    perce_ret = round(((p_value * total) / 100))
    print(f'{perce_ret} <--> {p_value} --> {total}')
    return perce_ret

#a list of json with one key should be passed
def ids_json_to_ids_list(json_data):
    id_as_list = []
    for d_ in json_data:
        id_as_list.append(d_['ques_id'])
    return id_as_list

def create_auto_quiz():
    subjects_perc = [{'subject': '29', 'percentage': 60}, {'subject': '11', 'percentage': 40}]
    total_question = 32
    quiz_id = 1
    level = sorted([9, 9, 9])
    default_percentage__for_class_levels = sorted([50, 30, 20], key=int, reverse=True)
    grand_tot = 0
    total_question_ids = []
    for i in range(len(level)):
        print(
            f'\nfor class {level[i]} weightage % will be {default_percentage__for_class_levels[i]} of {total_question}-Questiosn')
        sub_tot = 0
        for sub in subjects_perc:
            subject_weightage_percentage_value = calculate_percentage_value(sub['percentage'], total_question)
            subject_weightage_percentage_value_for_iter_class = calculate_percentage_value(
                default_percentage__for_class_levels[i], subject_weightage_percentage_value)
            sub_tot = sub_tot + subject_weightage_percentage_value_for_iter_class
            print(
                f"{getCode.subjectById(sub['subject'])} {sub['percentage']}%, Percentage value =  {subject_weightage_percentage_value_for_iter_class}")
            print('---'*90)
            query = f"SELECT ques_id from mcqs where sub_id = {sub['subject']} AND class = {level[i]} ORDER BY RAND() LIMIT {subject_weightage_percentage_value_for_iter_class}"
            m_conn = mysql_conn.mysql_obj()
            data = m_conn.mysql_execute(query, fetch_result=True)
            ques_id_list = ids_json_to_ids_list(data)
            total_question_ids.extend(ques_id_list)
            print(ques_id_list)
            # if len(ques_id_list) < 1:
            #     break
            #get question list from quiz
            query_quiz = f"SELECT question_list from quiz where q_id = {quiz_id}"
            m_conn = mysql_conn.mysql_obj()
            data = m_conn.mysql_execute(query_quiz, fetch_result=True)

            print(data)
            print(ques_id_list)
            # if data[0]['question_list'] is not None:
            #     if len(data[0]['question_list']) > 1:
            #         ques_id_list.append(data[0]['question_list'])
            # add question list to quiz
            print(ques_id_list)
        print(sub_tot)
        grand_tot = grand_tot + sub_tot
    if grand_tot > total_question:
        exceeded_question_count = grand_tot - total_question
        # print(f'Question quantity increased by {exceeded_question_count}')
        # print(f'Removing {exceeded_question_count} question from the quiz')
    print(total_question_ids)
    query_add_q_l = f"UPDATE quiz SET question_list = '{total_question_ids}' where q_id = {quiz_id}"
    print(query_add_q_l)
    m_conn.mysql_execute(query_add_q_l, fetch_result=False)
    m_conn.commit()
    
# create_auto_quiz()
# create_auto_quiz()

def chdir(ftp_path, ftp_conn):
    dirs = [d for d in ftp_path.split('/') if d != '']
    for p in dirs:
        check_dir(p, ftp_conn)

def check_dir(dir, ftp_conn):
    filelist = []
    ftp_conn.retrlines('LIST', filelist.append)
    found = False
    for f in filelist:
        if f.split()[-1] == dir and f.lower().startswith('d'):
            found = True
    if not found:
        ftp_conn.mkd(dir)
    ftp_conn.cwd(dir)


