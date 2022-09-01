import json

from fastapi import FastAPI
from fastapi import Request
from fastapi.middleware.cors import CORSMiddleware
from utilities import mysql_conn
from fastapi.encoders import jsonable_encoder
import re

from utilities.response import returnResponse

responseHandler = returnResponse()
mysql_handler = mysql_conn.mysql_obj()

app = FastAPI()
origins = ["http://localhost:4200"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# add to stock

@app.post("/generate-token")
async def generate_token(request: Request):
    body = await request.json()
    reg_id = int(re.search(r'\d+', body['regId']).group())
    password = body['password']
    query = f"SELECT * from users WHERE regId  = '{reg_id}' AND password = '{password}'"
    data = mysql_handler.mysql_execute(query, fetch_result=True)
    if not data:
        return responseHandler.responseBody(status_code='3001', msg="Invalid Credentials")
    return responseHandler.responseBody(status_code='2001', data=data)
    # return payload


@app.get("/category")
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
    query = f"INSERT INTO quiz (title,description,max_marks,no_of_ques,active,cat_id) VALUES ('{body['title']}','{body['description']}'," \
            f"'{body['maxMarks']}','{body['numberOfQuestions']}',{body['active']},'{body['cat_id']}')"
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
    query = f"INSERT INTO mcqs (q_id,content,opt1,opt2,opt3,opt4,ans,added_by) VALUES ('{body['q_id']}','{body['content']}'," \
            f"'{body['option1']}','{body['option2']}','{body['option3']}','{body['option4']}','{body['answer']}','{body['added_by']}')"
    print(query)
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


# show checked answer sheet
#
@app.post("/get/answer-sheet")
async def get_evaluated_answer_sheet(request: Request):
    body = await request.json()
    quiz_id = body['q_id']
    student_id = body['student_id']
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
        print(questions_data)
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
        final_response['student_id'] = student_id
        final_response['quiz_id'] = quiz_id
        final_response['total_question'] = total_question
        final_response['no_of_correct_answers'] = correct_answer
        final_response['total_attempted'] = total_attempted
        final_response['answer_data'] = questions_data
        return final_response



    else:
        return responseHandler.responseBody(status_code='3016', data=questions_data)
