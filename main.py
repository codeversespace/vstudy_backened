import json

from fastapi import FastAPI, Depends, File, UploadFile, Body
from fastapi import Request
from fastapi.middleware.cors import CORSMiddleware
from utilities import mysql_conn
import re
from utilities.response import returnResponse
from fastapi.security import OAuth2PasswordBearer
import xlrd


from app.model import PostSchema, UserSchema, UserLoginSchema
from app.auth.auth_bearer import JWTBearer
from app.auth.auth_handler import signJWT

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
responseHandler = returnResponse()
mysql_handler = mysql_conn.mysql_obj()

@app.get("/items/")
async def read_items(token: str = Depends(oauth2_scheme)):
    return {"token": token}


# @app.post("/user/upload")
# async def create_file(file: bytes = File()):
#     return {"file_size": len(file)}

def excel_to_db(excel_path, table: str, columns: list = []):
    #read excel
    excel_sheet =xlrd.open_workbook(excel_path)
    sheet_name = excel_sheet.sheet_names()
    for sh in range(0,len(sheet_name)):
        sheet = excel_sheet.sheet_by_index(sh)
        row_values = ''
        for r in range(1,sheet.nrows):
            row_value = ''
            for i in range(len(columns)):
                row_value = row_value + f'{sheet.cell(r,i).value},'
            row_value = f"({row_value.rstrip(',')})"
            row_values = row_values + ','+row_value
        final_value_set = (row_values.lstrip(','))
    cols =''
    a = final_value_set.replace('(',"('")
    b = a.replace(',',"','")
    c = b.replace(")','(",'),(')
    d = c.replace(")","')")
    e = d.replace('.0','')
    for i in range(len(columns)):
        if i > 0 :
            act_col = ',' + columns[i]
        else :
            act_col = columns[i]
        cols = cols + act_col
    query = f"INSERT INTO {table} ({cols}) VALUES {e}"
    # print(query)
    mysql_handler.mysql_execute(query, fetch_result=False)
    mysql_handler.commit()




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
        excel_to_db(f'assets/registration-data/{file.filename}', 'users', ['regId', 'name','class','school','email','phone','password','role'])

    return {"message": f"Successfully uploaded {file.filename}"}




origins = ["http://localhost:4200"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# export db
def export_db():
    cur = mysql_handler.mysql_cursor()

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
    filename = "backup_vsd_dev.sql"

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
    data = mysql_handler.mysql_execute(query, fetch_result=True)
    jwt_token = signJWT(reg_id)
    print(jwt_token)
    if not data:
        return responseHandler.responseBody(status_code='3001', msg="Invalid Credentials")
    return responseHandler.responseBody(status_code='2001', data=data, jwt  = jwt_token)
    # return payload


@app.get("/category", dependencies=[Depends(JWTBearer())])
async def get_categories():
    query = f"SELECT * from categories"
    data = mysql_handler.mysql_execute(query, fetch_result=True)
    if not data:
        return responseHandler.responseBody(status_code='3002')
    return responseHandler.responseBody(status_code='2002', data=data)




@app.get("/quiz")
async def get_categories():
    query = f"SELECT * FROM quiz INNER JOIN categories ON categories.cat_id=quiz.cat_id"
    data = mysql_handler.mysql_execute(query, fetch_result=True)
    if not data:
        return responseHandler.responseBody(status_code='3003')
    return responseHandler.responseBody(status_code='2003', data=data)


@app.get("/quiz/active")
async def get_categories():
    query = f"SELECT * FROM quiz INNER JOIN categories ON categories.cat_id=quiz.cat_id WHERE quiz.active=1"
    data = mysql_handler.mysql_execute(query, fetch_result=True)
    if not data:
        return responseHandler.responseBody(status_code='3004')
    return responseHandler.responseBody(status_code='2004', data=data)


# http://localhost:8000/quiz/category/active/1
@app.get("/quiz/category/active/{cat_id}")
async def get_category(cat_id: str):
    query = f"SELECT * FROM quiz INNER JOIN categories ON categories.cat_id=quiz.cat_id WHERE quiz.active=1 AND quiz.cat_id={cat_id}"
    data = mysql_handler.mysql_execute(query, fetch_result=True)
    if not data:
        return responseHandler.responseBody(status_code='3005')
    return responseHandler.responseBody(status_code='2005', data=data)


# get all questions of a given category
@app.get("/category/questions/{cat_id}")
async def get_questions_from_category(cat_id: str):
    query = f"SELECT * FROM mcqs INNER JOIN quiz ON quiz.q_id = mcqs.q_id where quiz.cat_id = {cat_id};"
    data = mysql_handler.mysql_execute(query, fetch_result=True)
    if not data:
        return responseHandler.responseBody(status_code='3006')
    return responseHandler.responseBody(status_code='2006', data=data)


# get all questions of a given quiz
@app.get("/question/quiz/{quiz_id}")
async def get_questions_from_quiz_id(quiz_id: str):
    query = f"SELECT q_id,ques_id,content,opt1,opt2,opt3,opt4 FROM mcqs where q_id = {quiz_id};"
    data = mysql_handler.mysql_execute(query, fetch_result=True)
    if not data:
        return responseHandler.responseBody(status_code='3007')
    return responseHandler.responseBody(status_code='2007', data=data)


@app.get("/question/quiz/all/{quiz_id}")
async def get_questions_from_quiz_id(quiz_id: str):
    query = f"SELECT * FROM mcqs where q_id = {quiz_id};"
    data = mysql_handler.mysql_execute(query, fetch_result=True)
    if not data:
        return responseHandler.responseBody(status_code='3007')
    return responseHandler.responseBody(status_code='2007', data=data)


@app.get("/quiz/{id}")
async def get_quiz_detail(id: str):
    query = f"SELECT * FROM quiz WHERE q_id = {id}"
    data = mysql_handler.mysql_execute(query, fetch_result=True)
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
    mysql_handler.mysql_execute(query, fetch_result=False)
    mysql_handler.commit()
    if mysql_handler.mysql_cursor().rowcount < 1:
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
    mysql_handler.mysql_execute(query, fetch_result=False)
    mysql_handler.commit()
    if mysql_handler.mysql_cursor().rowcount < 1:
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
    mysql_handler.mysql_execute(query, fetch_result=False)
    mysql_handler.commit()
    if mysql_handler.mysql_cursor().rowcount < 1:
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
    mysql_handler.mysql_execute(query, fetch_result=False)
    mysql_handler.commit()
    if mysql_handler.mysql_cursor().rowcount < 1:
        data["status"] = "failed to add subject"
        return responseHandler.responseBody(status_code='3011', data=data)
    data["status"] = "Subject added"
    return responseHandler.responseBody(status_code='2011', data=data)


@app.get("/subject")
async def get_subject():
    query = f"SELECT * FROM subject"
    data = mysql_handler.mysql_execute(query, fetch_result=True)
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
    mysql_handler.mysql_execute(query, fetch_result=False)
    mysql_handler.commit()
    if mysql_handler.mysql_cursor().rowcount < 1:
        data["status"] = "failed to add level"
        return responseHandler.responseBody(status_code='3013', data=data)
    data["status"] = "Level added"
    return responseHandler.responseBody(status_code='2013', data=data)


@app.get("/level")
async def get_level():
    query = f"SELECT * FROM level"
    data = mysql_handler.mysql_execute(query, fetch_result=True)
    if not data:
        return responseHandler.responseBody(status_code='3014')
    return responseHandler.responseBody(status_code='2014', data=data)


#
@app.post("/add/submit_ans")
async def submit_answer(request: Request):
    data = {}
    body = await request.json()
    ans_data = json.dumps(body['data'])
    query = f"INSERT INTO ans_sheet VALUES ({body['stu_id']},{body['q_id']},'{ans_data}')"
    print(query)
    mysql_handler.mysql_execute(query, fetch_result=False)
    mysql_handler.commit()
    if mysql_handler.mysql_cursor().rowcount < 1:
        data["status"] = "failed to submit answer keys"
        return responseHandler.responseBody(status_code='3015', data=data)
    data["status"] = "Answer sheet submitted"
    return responseHandler.responseBody(status_code='2015', data=data)


# {reg_id: "5249962"}


@app.post("/user/is-exist")
async def check_if_user_exist(request: Request):
    body = await request.json()
    registration_id = body['reg_id']
    return mysql_handler.if_exist('users', ['regId'], [registration_id])


# register a user
@app.post("/user")
async def register_user(request: Request):
    data = {}
    body = await request.json()
    query = f"INSERT INTO users (regId,name,class,school,email,phone,password,role) " \
            f"VALUES ({body['regId']},'{body['name']}',{body['class']},{body['school']},'{body['email']}',{body['phone']},'{body['password']}','student')"
    # {"regId": "123", "name": "Syed Abdullah", "class": 1, "school": "09890", "email": "sayedabdullah11@gmail.com",
    #  "phone": 919199191, "password": "123"}
    mysql_handler.mysql_execute(query, fetch_result=False)
    mysql_handler.commit()
    if mysql_handler.mysql_cursor().rowcount < 1:
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
    if not mysql_handler.if_exist('ans_sheet', ['student_id', 'q_id'], [student_id, quiz_id]):
        data = {''}
        return responseHandler.responseBody(status_code='3017',
                                            msg=f'No record found for the pair [student_id:{student_id} - quiz_id:{quiz_id}',
                                            data=data)

    # first fecth submitted answer from db
    # then fetch the question data from db
    query = f"SELECT ques_id, content,opt1,opt2,opt3,opt4,ans FROM mcqs where q_id = {quiz_id};"
    questions_data = mysql_handler.mysql_execute(query, fetch_result=True)

    # mysql_handler.close()
    if questions_data:
        # question found
        query_ans = f"SELECT ans_keys from ans_sheet WHERE student_id = {student_id} AND q_id = {quiz_id}"
        answer_data = mysql_handler.mysql_execute(query_ans, fetch_result=True)
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
