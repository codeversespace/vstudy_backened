import json

from utilities import mysql_conn
from fastapi import  Request, APIRouter

from utilities.response import returnResponse

router =  APIRouter()
responseHandler = returnResponse()


@router.post("/add/submit_ans")
async def submit_answer(request: Request):
    data = {}
    m_conn = mysql_conn.mysql_obj()
    body = await request.json()
    ans_data = json.dumps(body['data'])
    query = f"UPDATE ans_sheet SET ans_keys = '{ans_data}' WHERE student_id = {body['stu_id']} AND q_id = {body['q_id']}"
    print(query)
    m_conn.mysql_execute(query, fetch_result=False)
    m_conn.commit()
    if m_conn.mysql_cursor().rowcount < 1:
        data["status"] = "failed to submit answer keys"
        return responseHandler.responseBody(status_code='3015', data=data)
    data["status"] = "Answer sheet submitted"
    return responseHandler.responseBody(status_code='2015', data=data)


# show checked answer sheet
#
@router.post("/get/answer-sheet")
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
