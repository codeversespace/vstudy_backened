import json
import time

from fastapi import FastAPI, Depends, UploadFile
from fastapi import Request
from fastapi.middleware.cors import CORSMiddleware
from utilities import mysql_conn
import re
from utilities.response import returnResponse

from fastapi.security import OAuth2PasswordBearer
import xlrd
from app.auth.auth_bearer import JWTBearer
from app.auth.auth_handler import signJWT

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
responseHandler = returnResponse()


@app.get("/items/")
async def read_items(token: str = Depends(oauth2_scheme)):
    return {"token": token}


# @app.post("/user/upload")
# async def create_file(file: bytes = File()):
#     return {"file_size": len(file)}

def excel_to_db(excel_path, table: str, columns: list = []):
    # read excel
    excel_sheet = xlrd.open_workbook(excel_path)
    sheet_name = excel_sheet.sheet_names()
    for sh in range(0, len(sheet_name)):
        sheet = excel_sheet.sheet_by_index(sh)
        row_values = ''
        for r in range(1, sheet.nrows):
            row_value = ''
            for i in range(len(columns)):
                row_value = row_value + f'{sheet.cell(r, i).value},'
            row_value = f"({row_value.rstrip(',')})"
            row_values = row_values + ',' + row_value
        final_value_set = (row_values.lstrip(','))
    cols = ''
    a = final_value_set.replace('(', "('")
    b = a.replace(',', "','")
    c = b.replace(")','(", '),(')
    d = c.replace(")", "')")
    e = d.replace('.0', '')
    for i in range(len(columns)):
        if i > 0:
            act_col = ',' + columns[i]
        else:
            act_col = columns[i]
        cols = cols + act_col
    query = f"INSERT INTO {table} ({cols}) VALUES {e}"
    # print(query)
    mysql_conn.mysql_obj().mysql_execute(query, fetch_result=False)
    mysql_conn.mysql_obj().commit()
    mysql_conn.mysql_obj().close()


@app.post("/user/upload")
async def create_upload_file(file: UploadFile):
    try:
        contents = file.file.read()
        with open(f'assets/registration-data/{file.filename}', 'wb') as f:
            f.write(contents)
    except Exception:
        return {"message": "There was an error uploading the file"}
    finally:
        file.file.close()
        excel_to_db(f'assets/registration-data/{file.filename}', 'users',
                    ['regId', 'name', 'class', 'school', 'email', 'phone', 'password', 'role'])

    return {"message": f"Successfully uploaded {file.filename}"}


origins = ["http://localhost"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup():
    # if not mysql_conn.mysql_obj().mysql_cursor():
    print('Checking app health')


# export db
def export_db():
    cur = mysql_conn.mysql_obj().mysql_cursor()

    cur.execute("SHOW TABLES")
    data = ""
    tables = []
    for table in cur.fetchall():
        tables.append(table[0])

    for table in tables:
        data += "DROP TABLE IF EXISTS `" + str(table) + "`;"

        cur.execute("SHOW CREATE TABLE `" + str(table) + "`;")
        data += "\n" + str(cur.fetchone()[1]) + ";\n\n"

        cur.execute("SELECT * FROM `" + str(table) + "`;")
        for row in cur.fetchall():
            data += "INSERT INTO `" + str(table) + "` VALUES("
            first = True
            for field in row:
                if not first:
                    data += ', '
                data += '"' + str(field) + '"'
                first = False

            data += ");\n"
        data += "\n\n"

    # now = datetime.datetime.now()
    filename = "vstudy_dev.sql"

    FILE = open(filename, "w+")
    FILE.writelines(data)
    FILE.close()


@app.post("/generate-token", tags=['Generate Token'])
async def generate_token(request: Request):
    # return token
    body = await request.json()

    reg_id = int(re.search(r'\d+', body['regId']).group())
    password = body['password']
    query = f"SELECT * from users WHERE regId  = '{reg_id}' AND password = '{password}'"
    data = mysql_conn.mysql_obj().mysql_execute(query, fetch_result=True)
    mysql_conn.mysql_obj().close()

    jwt_token = signJWT(reg_id)
    if not data:
        return responseHandler.responseBody(status_code='3001', msg="Invalid Credentials")
    return responseHandler.responseBody(status_code='2001', data=data, jwt=jwt_token)
    # return payload


@app.get("/category", dependencies=[Depends(JWTBearer())])
async def get_categories():
    query = f"SELECT * from categories"
    data = mysql_conn.mysql_obj().mysql_execute(query, fetch_result=True)
    if not data:
        return responseHandler.responseBody(status_code='3002')
    return responseHandler.responseBody(status_code='2002', data=data)


@app.get("/quiz")
async def get_categories():
    query = f"SELECT * FROM quiz INNER JOIN categories ON categories.cat_id=quiz.cat_id"
    data = mysql_conn.mysql_obj().mysql_execute(query, fetch_result=True)
    if not data:
        return responseHandler.responseBody(status_code='3003')
    return responseHandler.responseBody(status_code='2003', data=data)


@app.get("/quiz/active")
async def get_categories():
    query = f"SELECT * FROM quiz INNER JOIN categories ON categories.cat_id=quiz.cat_id WHERE quiz.active=1"
    data = mysql_conn.mysql_obj().mysql_execute(query, fetch_result=True)
    if not data:
        return responseHandler.responseBody(status_code='3004')
    return responseHandler.responseBody(status_code='2004', data=data)


# http://localhost:8000/quiz/category/active/1
@app.get("/quiz/category/active/{cat_id}")
async def get_category(cat_id: str):
    query = f"SELECT * FROM quiz INNER JOIN categories ON categories.cat_id=quiz.cat_id WHERE quiz.active=1 AND quiz.cat_id={cat_id}"
    data = mysql_conn.mysql_obj().mysql_execute(query, fetch_result=True)
    if not data:
        return responseHandler.responseBody(status_code='3005')
    return responseHandler.responseBody(status_code='2005', data=data)


# get all questions of a given category
@app.get("/category/questions/{cat_id}")
async def get_questions_from_category(cat_id: str):
    query = f"SELECT * FROM mcqs INNER JOIN quiz ON quiz.q_id = mcqs.q_id where quiz.cat_id = {cat_id};"
    data = mysql_conn.mysql_obj().mysql_execute(query, fetch_result=True)
    if not data:
        return responseHandler.responseBody(status_code='3006')
    return responseHandler.responseBody(status_code='2006', data=data)


# get all questions of a given quiz
@app.get("/question/quiz/{quiz_id}")
async def get_questions_from_quiz_id(quiz_id: str):
    query = f"SELECT q_id,ques_id,content,opt1,opt2,opt3,opt4 FROM mcqs where q_id = {quiz_id};"
    data = mysql_conn.mysql_obj().mysql_execute(query, fetch_result=True)
    if not data:
        return responseHandler.responseBody(status_code='3007')
    return responseHandler.responseBody(status_code='2007', data=data)


@app.get("/question/quiz/all/{quiz_id}")
async def get_questions_from_quiz_id(quiz_id: str):
    query = f"SELECT * FROM mcqs where q_id = {quiz_id};"
    data = mysql_conn.mysql_obj().mysql_execute(query, fetch_result=True)
    if not data:
        return responseHandler.responseBody(status_code='3007')
    return responseHandler.responseBody(status_code='2007', data=data)


@app.get("/quiz/{id}")
async def get_quiz_detail(id: str):
    query = f"SELECT * FROM quiz WHERE q_id = {id}"
    data = mysql_conn.mysql_obj().mysql_execute(query, fetch_result=True)
    if not data:
        return responseHandler.responseBody(status_code='3003')
    return responseHandler.responseBody(status_code='2003', data=data)


##########
# INSERT #
##########
@app.post("/add/category")
async def add_category(request: Request):
    data = {}
    body = await request.json()
    query = f"INSERT INTO categories (cat_title,cat_desc) VALUES ('{body['title']}','{body['description']}')"
    mysql_conn.mysql_obj().mysql_execute(query, fetch_result=False)
    mysql_conn.mysql_obj().commit()
    if mysql_conn.mysql_obj().mysql_cursor().rowcount < 1:
        data["status"] = "failed to insert"
        return responseHandler.responseBody(status_code='3008', data=data)
    data["status"] = "Category added"
    return responseHandler.responseBody(status_code='2008', data=data)


# if __name__ == "__main__":
#     uvicorn.run(app, host="127.0.0.1", port=5049)

@app.post("/add/quiz")
async def add_quiz(request: Request):
    data = {}
    body = await request.json()
    query = f"INSERT INTO quiz (title,description,max_marks,no_of_ques,active,cat_id,level_id) VALUES ('{body['title']}','{body['description']}'," \
            f"'{body['maxMarks']}','{body['numberOfQuestions']}',{body['active']},'{body['cat_id']}','{body['level_id']}')"
    print(query)
    mysql_conn.mysql_obj().mysql_execute(query, fetch_result=False)
    mysql_conn.mysql_obj().commit()
    if mysql_conn.mysql_obj().mysql_cursor().rowcount < 1:
        data["status"] = "failed to insert quiz"
        return responseHandler.responseBody(status_code='3008', data=data)
    data["status"] = "Quiz added"
    return responseHandler.responseBody(status_code='2008', data=data)


@app.post("/add/question")
async def add_quiz(request: Request):
    data = {}
    body = await request.json()
    # will get added by value from UI
    query = f"INSERT INTO mcqs (q_id,content,opt1,opt2,opt3,opt4,ans,added_by,sub_id,class) VALUES ('{body['q_id']}','{body['content']}'," \
            f"'{body['option1']}','{body['option2']}','{body['option3']}','{body['option4']}','{body['answer']}','{body['added_by']}',{body['sub_id']},{body['class']})"
    mysql_conn.mysql_obj().mysql_execute(query, fetch_result=False)
    mysql_conn.mysql_obj().commit()
    if mysql_conn.mysql_obj().mysql_cursor().rowcount < 1:
        data["status"] = "failed to add question"
        return responseHandler.responseBody(status_code='3008', data=data)
    data["status"] = "question added"
    return responseHandler.responseBody(status_code='2008', data=data)


# get questions from quiz id


# add subject
@app.post("/add/subject")
async def add_subject(request: Request):
    data = {}
    body = await request.json()
    query = f"INSERT INTO subject (sub_title,sub_desc) VALUES ('{body['title']}','{body['description']}')"
    mysql_conn.mysql_obj().mysql_execute(query, fetch_result=False)
    mysql_conn.mysql_obj().commit()
    if mysql_conn.mysql_obj().mysql_cursor().rowcount < 1:
        data["status"] = "failed to add subject"
        return responseHandler.responseBody(status_code='3011', data=data)
    data["status"] = "Subject added"
    return responseHandler.responseBody(status_code='2011', data=data)


@app.get("/subject")
async def get_subject():
    query = f"SELECT * FROM subject"
    data = mysql_conn.mysql_obj().mysql_execute(query, fetch_result=True)
    if not data:
        return responseHandler.responseBody(status_code='3012')
    return responseHandler.responseBody(status_code='2012', data=data)


# add level
@app.post("/add/level")
async def add_subject(request: Request):
    data = {}
    body = await request.json()
    query = f"INSERT INTO level (level_title,level_desc,level_class) VALUES ('{body['title']}','{body['description']}','{body['class']}')"
    print(query)
    mysql_conn.mysql_obj().mysql_execute(query, fetch_result=False)
    mysql_conn.mysql_obj().commit()
    if mysql_conn.mysql_obj().mysql_cursor().rowcount < 1:
        data["status"] = "failed to add level"
        return responseHandler.responseBody(status_code='3013', data=data)
    data["status"] = "Level added"
    return responseHandler.responseBody(status_code='2013', data=data)


@app.get("/level")
async def get_level():
    query = f"SELECT * FROM level"
    data = mysql_conn.mysql_obj().mysql_execute(query, fetch_result=True)
    if not data:
        return responseHandler.responseBody(status_code='3014')
    return responseHandler.responseBody(status_code='2014', data=data)


#
@app.post("/add/submit_ans-1")
async def submit_answer_1(request: Request):
    data = {}
    body = await request.json()
    ans_data = json.dumps(body['data'])
    query = f"UPDATE ans_sheet SET ans_keys = '{ans_data}' WHERE student_id = {body['stu_id']} AND q_id = {body['q_id']}"
    print(query)
    m = mysql_conn.mysql_obj()
    m.mysql_execute(query, fetch_result=False)
    m.commit()
    if m.mysql_cursor().rowcount < 1:
        data["status"] = "failed to submit answer keys"
        return responseHandler.responseBody(status_code='3015', data=data)
    data["status"] = "Answer sheet submitted"
    return responseHandler.responseBody(status_code='2015', data=data)


# {reg_id: "5249962"}


@app.post("/user/is-exist")
async def check_if_user_exist(request: Request):
    body = await request.json()
    registration_id = body['reg_id']
    return mysql_conn.mysql_obj().if_exist('users', ['regId'], [registration_id])


# register a user
@app.post("/user")
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


# show checked answer sheet
#
@app.post("/get/answer-sheet")
async def get_evaluated_answer_sheet(request: Request):
    body = await request.json()
    quiz_id = body['q_id']
    student_id = body['stu_id']
    # check if any quiz for given stu_id present in answer_db
    if not mysql_conn.mysql_obj().if_exist('ans_sheet', ['student_id', 'q_id'], [student_id, quiz_id]):
        data = {''}
        return responseHandler.responseBody(status_code='3017',
                                            msg=f'No record found for the pair [student_id:{student_id} - quiz_id:{quiz_id}',
                                            data=data)

    # first fecth submitted answer from db
    # then fetch the question data from db
    query = f"SELECT ques_id, content,opt1,opt2,opt3,opt4,ans FROM mcqs where q_id = {quiz_id};"
    questions_data = mysql_conn.mysql_obj().mysql_execute(query, fetch_result=True)

    # mysql_conn.mysql_obj().close()
    if questions_data:
        # question found
        query_ans = f"SELECT ans_keys from ans_sheet WHERE student_id = {student_id} AND q_id = {quiz_id}"
        answer_data = mysql_conn.mysql_obj().mysql_execute(query_ans, fetch_result=True)
        answer_list = json.loads(answer_data[0]['ans_keys'])
        correct_answer = 0
        total_question = len(questions_data)
        # return answer_list, question_data
        total_attempted = total_question
        for ques_no in range(total_question):
            # check if not attempted
            if str(questions_data[ques_no]['ques_id']) not in answer_list:
                questions_data[ques_no]['result'] = 'un_attempted'
                total_attempted -= 1
            else:
                selected_answer = answer_list[str(questions_data[ques_no]['ques_id'])].lower()
                if questions_data[ques_no]['ans'].lower() == selected_answer:
                    # correct answer
                    correct_answer += 1
                    questions_data[ques_no]['result'] = 'right'
                else:
                    questions_data[ques_no]['result'] = 'wrong'
                    questions_data[ques_no]['selected_answer'] = selected_answer
            if ques_no >= len(answer_list):
                break
        final_response = {}
        final_response['stu_id'] = student_id
        final_response['quiz_id'] = quiz_id
        final_response['total_question'] = total_question
        final_response['no_of_correct_answers'] = correct_answer
        final_response['total_attempted'] = total_attempted
        final_response['answer_data'] = questions_data
        return final_response
    else:
        return responseHandler.responseBody(status_code='3016', data=questions_data)


@app.post("/ans/get-quiz-start-time")
async def get_quiz_start_time_and(request: Request):
    body = await request.json()
    q_id = body['q_id']
    stu_id = body['stu_id']
    m_conn = mysql_conn.mysql_obj()
    query = f"SELECT quiz.time_per_qstn_ms, ans_sheet.started_at FROM quiz RIGHT JOIN ans_sheet ON quiz.q_id=ans_sheet.q_id WHERE ans_sheet.student_id = {stu_id} AND ans_sheet.q_id ={q_id}"
    data = m_conn.mysql_execute(query, fetch_result=True)
    if not data:
        # insert quiz startup data
        curr_time_ms = int(time.time() * 1000.0)
        query = f"INSERT INTO ans_sheet (student_id,q_id,started_at) VALUES ({stu_id},{q_id},{curr_time_ms})"
        m_conn.mysql_execute(query, fetch_result=False)
        m_conn.commit()
        query = f"SELECT quiz.time_per_qstn_ms, ans_sheet.started_at FROM quiz RIGHT JOIN ans_sheet ON quiz.q_id=ans_sheet.q_id WHERE ans_sheet.student_id = {stu_id} AND ans_sheet.q_id ={q_id}"
        data = m_conn.mysql_execute(query, fetch_result=True)
    m_conn.close()
    return responseHandler.responseBody(status_code='2003', data=data)


# {"stu_id":"124","q_id":"1","data":{"1":"opt1","2":"opt2"}}
@app.post("/add/submit_ans")
async def submit_answer(request: Request):
    data = {}
    m_conn = mysql_conn.mysql_obj()
    body = await request.json()
    ans_data = json.dumps(body['data'])
    student_id = body['stu_id']
    quiz_id = body['q_id']
    question_attempted, marks_obtained, answer_data = __evaluate_answer_sheet(m_conn, quiz_id, student_id, ans_data)
    print(question_attempted)
    query = f"UPDATE ans_sheet SET ans_keys = '{answer_data}', marks_obtained = {marks_obtained} WHERE student_id = {student_id} AND q_id = {quiz_id}"
    m_conn.mysql_execute(query, fetch_result=False)
    m_conn.commit()
    if m_conn.mysql_cursor().rowcount < 1:
        data["status"] = "failed to submit answer keys"
        m_conn.close()
        return responseHandler.responseBody(status_code='3015', data=data)
    data["status"] = "Answer sheet submitted"
    m_conn.close()
    return responseHandler.responseBody(status_code='2015', data=data)


# show checked answer sheet
#
# @router.post("/get/answer-sheet")
# async def get_evaluated_answer_sheet(request: Request):
#     body = await request.json()
#     quiz_id = body['q_id']
#     student_id = body['stu_id']
#     m_conn = mysql_conn.mysql_obj()
#     if not m_conn.if_exist('ans_sheet', ['student_id', 'q_id'], [student_id, quiz_id]):
#         data = {''}
#         return responseHandler.responseBody(status_code='3017',
#                                             msg=f'No record found for the pair [student_id:{student_id} - quiz_id:{quiz_id}',
#                                             data=data)
#     return __evaluate_answer_sheet(m_conn, quiz_id, student_id)


def __evaluate_answer_sheet(m_conn, quiz_id: str = None, student_id: str = None, answer_data: dict = {}):
    query = f"SELECT ques_id, content,opt1,opt2,opt3,opt4,ans FROM mcqs where q_id = {quiz_id};"
    questions_data = m_conn.mysql_execute(query, fetch_result=True)

    # mysql_conn.mysql_obj().close()
    if questions_data:
        # question found
        no_of_correct_answer = 0
        total_question = len(questions_data)
        # return answer_list, question_data
        answer_data = json.loads(answer_data)
        question_attempted = len(answer_data)
        for ques_no in range(total_question):
            # check if not attempted
            ques_id = str(questions_data[ques_no]['ques_id'])
            correct_option = questions_data[ques_no]['ans'].lower()
            if ques_no >= len(answer_data):
                break
            answer_data[ques_id].append(correct_option)
            if ques_id not in answer_data:
                answer_data[str(ques_no)].append('')
            else:
                selected_answer = answer_data[ques_id][0].lower()
                if correct_option == selected_answer:
                    no_of_correct_answer += 1

        return question_attempted, no_of_correct_answer, json.dumps(answer_data)
    else:
        return responseHandler.responseBody(status_code='3016', data=questions_data)


def fetch_submitted_answer_sheet(student_id: str = None, quiz_id: str = None):
    m_conn = mysql_conn.mysql_obj()
    query = f"SELECT quiz.q_id, quiz.title,quiz.max_marks,quiz.no_of_ques, ans_sheet.ans_keys, ans_sheet.marks_obtained FROM quiz INNER JOIN " \
            f"ans_sheet ON quiz.q_id=ans_sheet.q_id where ans_sheet.q_id={quiz_id} AND ans_sheet.student_id={student_id};"
    quiz = m_conn.mysql_execute(query, fetch_result=True)
    q = f"SELECT ques_id, content,opt1,opt2,opt3,opt4 from mcqs WHERE q_id = {quiz_id}"
    questions_data = m_conn.mysql_execute(q, fetch_result=True)
    m_conn.close()
    a_k = quiz[0]['ans_keys']
    marks_obtained = quiz[0]['marks_obtained']
    ans_keys = json.loads(a_k)
    final_response = {}
    for i in range(len(questions_data)):
        selected_option = ans_keys[str(questions_data[i]['ques_id'])][0]
        correct_option = ans_keys[str(questions_data[i]['ques_id'])][1]
        questions_data[i]['selected_option'] = selected_option
        questions_data[i]['correct_option'] = correct_option
    final_response['stu_id'] = student_id
    final_response['quiz_id'] = quiz_id
    final_response['total_question'] = quiz[0]['no_of_ques']
    final_response['marks_obtained'] = marks_obtained
    # final_response['no_of_correct_answers'] = no_of_correct_answer  # marks_obtained
    # final_response['total_attempted'] = question_attempted
    final_response['answer_data'] = questions_data
    return responseHandler.responseBody(status_code='2016', data=final_response)