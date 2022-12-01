class returnResponse:
    def __generate_response_msg_from_code(self, status_code: str):
        body = {}
        body["code"] = status_code
        if status_code == '1':
            body["message"] = "Default success msg"
        if status_code.startswith("2"):
            body["status"] = "success"
            if status_code == "2001":
                body["message"] = "Login successful"
            if status_code == "2002":
                body["message"] = "Category fetched"
            if status_code == "2003":
                body["message"] = "Quiz fetched"
            if status_code == "2004":
                body["message"] = "Active quiz found"
            if status_code == "2005":
                body["message"] = "active quiz for given category found"
            if status_code == "2006":
                body["message"] = "Quesiton for given category found"
            if status_code == "2007":
                body["message"] = "Quesiton for given quiz id found"
            if status_code == "2008":
                body["message"] = "Category added"
            if status_code == "2009":
                body["message"] = "Quiz added"
            if status_code == "2010":
                body["message"] = "Question added"
            if status_code == "2011":
                body["message"] = "Subject added"
            if status_code == "2012":
                body["message"] = "Subject fetched"
            if status_code == "2013":
                body["message"] = "Level added"
            if status_code == "2014":
                body["message"] = "Level fetched"
            if status_code == "2015":
                body["message"] = "Answer sheet submitted"
            if status_code == "2016":
                body["message"] = "Questions found for the qiven quiz/answer-sheet"
            if status_code == "2017":
                body["message"] = "Student_id<->Quiz_id Record found"
            if status_code == "2018":
                body["message"] = "Student registration done"
            if status_code == "2019":
                body["message"] = "Question set added"
            if status_code == "2020":
                body["message"] = "Certificate found"


        else:
            body["status"] = "failure"
            if status_code == "3999":
                body["message"] = "Unable to process your request, un-authorised access."
            if status_code == "3001":
                body["message"] = "Login failed"
            if status_code == "3002":
                body["message"] = "No category found"
            if status_code == "3003":
                body["message"] = "No quiz found"
            if status_code == "3004":
                body["message"] = "No active quiz found"
            if status_code == "3005":
                body["message"] = "No active quiz for given category found"
            if status_code == "3006":
                body["message"] = "No quesiton for given category found"
            if status_code == "3007":
                body["message"] = "No quesiton for given quiz id can be found"
            if status_code == "3008":
                body["message"] = "Category not added"
            if status_code == "3009":
                body["message"] = "Quiz not added"
            if status_code == "3010":
                body["message"] = "Question not added"
            if status_code == "3011":
                body["message"] = "Subject not added"
            if status_code == "3012":
                body["message"] = "Subject not fetched"
            if status_code == "3013":
                body["message"] = "Level not added"
            if status_code == "3014":
                body["message"] = "Level not fetched"
            if status_code == "3015":
                body["message"] = "Answer sheet not submitted"
            if status_code == "3016":
                body["message"] = "No questions can be found for the qiven quiz/answer-sheet"
            if status_code == "3017":
                body["message"] = "Student_id<->Quiz_id Record not found"
            if status_code == "3018":
                body["message"] = "Student registration failed"
            if status_code == "3403":
                body["message"] = "Session expired"
            if status_code == "3020":
                body["message"] = "Certificate not found"

        return body

    def responseBody(self, status_code: str, msg: str = None, data: dict = {}, jwt: str = None):
        body = self.__generate_response_msg_from_code(status_code)
        if jwt is not None:
            body["authentication_token"] = jwt
        body["reason"] = msg
        # if len(data) > 1:
        body["data"] = data
        return body
