import json

from app.api.v1.validator import if_request_valid
from app.auth.auth_bearer import JWTBearer
from app.auth.auth_handler import decodeJWT
from app.utilities import mysql_conn
from fastapi import Request, APIRouter, Depends,Header

from app.utilities.response import returnResponse

router = APIRouter()
responseHandler = returnResponse()

@router.post("/add/submit_ans",dependencies=[Depends(JWTBearer())])
async def submit_answer(request: Request, Authorization=Header(default=None)):
    data = {}
    m_conn = mysql_conn.mysql_obj()
    body = await request.json()
    ans_data = json.dumps(body['data'])
    student_id = body['stu_id']
    quiz_id = body['q_id']
    question_attempted, marks_obtained, answer_data = __evaluate_answer_sheet(m_conn, quiz_id, student_id, ans_data)

    if not if_request_valid('super', decodeJWT(Authorization.replace('Bearer ', ''))['user_id']):
        # if non admin
        query = f"UPDATE ans_sheet SET ans_keys = '{answer_data}', marks_obtained = {marks_obtained} WHERE student_id = {student_id} AND q_id = {quiz_id}"
    else :
        query = f"INSERT INTO ans_sheet (student_id,q_id,ans_keys,marks_obtained) VALUES ({student_id},{quiz_id} ,'{answer_data}',{marks_obtained})"


    m_conn.mysql_execute(query, fetch_result=False)
    m_conn.commit()
    data["status"] = "Answer sheet submitted"
    m_conn.close()
    return responseHandler.responseBody(status_code='2015', data=data)

def __evaluate_answer_sheet(m_conn, quiz_id: str = None, student_id: str = None, answer_data: dict = {}):
    query = f"SELECT ques_id, content,opt1,opt2,opt3,opt4,ans FROM mcqs where q_id = {quiz_id};"
    questions_data = m_conn.mysql_execute(query, fetch_result=True)

    # mysql_conn.mysql_obj().close()
    if questions_data:
        # question found
        no_of_correct_answer = 0
        total_question = len(questions_data)
        # return answer_list, question_data
        {3: ["opt1"]}
        answer_data = json.loads(answer_data)
        question_attempted = len(answer_data)
        for ques_no in range(total_question):
            # check if not attempted
            ques_id = str(questions_data[ques_no]['ques_id'])
            correct_option = questions_data[ques_no]['ans'].lower()
            if ques_no >= len(answer_data):
                break

            if ques_id not in answer_data:
                answer_data[ques_id].append('')
            else:
                answer_data[ques_id].append(correct_option)
                selected_answer = answer_data[ques_id][0].lower()
                if correct_option == selected_answer:
                    no_of_correct_answer += 1

        return question_attempted, no_of_correct_answer, json.dumps(answer_data)
    else:
        return responseHandler.responseBody(status_code='3016', data=questions_data)

@router.post("/get/answer-sheet",dependencies=[Depends(JWTBearer())])
async def fetch_submitted_answer_sheet(request: Request):
    body = await request.json()
    quiz_id = body['q_id']
    student_id = body['stu_id']
    m_conn = mysql_conn.mysql_obj()
    query = f"SELECT quiz.q_id, quiz.title,quiz.max_marks,quiz.no_of_ques, ans_sheet.ans_keys, ans_sheet.marks_obtained FROM quiz INNER JOIN " \
            f"ans_sheet ON quiz.q_id=ans_sheet.q_id where ans_sheet.q_id={quiz_id} AND ans_sheet.student_id={student_id};"
    quiz = m_conn.mysql_execute(query, fetch_result=True)
    q = f"SELECT ques_id, content,opt1,opt2,opt3,opt4 from mcqs WHERE q_id = {quiz_id}"
    questions_data = m_conn.mysql_execute(q, fetch_result=True)
    m_conn.close()
    a_k = quiz[0]['ans_keys']
    print(a_k)
    marks_obtained = quiz[0]['marks_obtained']
    ans_keys = json.loads(a_k)
    final_response = {}
    print(questions_data)
    for i in range(len(questions_data)):
        selected_option = ans_keys[str(questions_data[i]['ques_id'])][0]
        correct_option = ans_keys[str(questions_data[i]['ques_id'])][1]
        questions_data[i]['selected_option'] = selected_option
        questions_data[i]['correct_option'] = correct_option
    final_response['stu_id'] = student_id
    final_response['quiz_id'] = quiz_id
    final_response['total_question'] = quiz[0]['no_of_ques']
    final_response['marks_obtained'] = marks_obtained
    final_response['answer_data'] = questions_data
    return responseHandler.responseBody(status_code='2016', data=final_response)


@router.get("/result/get-ranking/{q_id}")
async def get_quiz_start_time_and(q_id:str):
    m_conn = mysql_conn.mysql_obj()
    query = f'select users.regId, ans_sheet.marks_obtained ,users.name from ans_sheet inner join users ON users.regId = ans_sheet.student_id where ans_sheet.marks_obtained is not null and q_id ={q_id} order by marks_obtained desc;'
    data = m_conn.mysql_execute(query, fetch_result=True)
    m_conn.close()
    return responseHandler.responseBody(status_code='2003', data=data)