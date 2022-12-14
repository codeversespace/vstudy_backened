class returnResponse:
    def __generate_response_msg_from_code(self, status_code: str):
        body = {}
        body["code"] = status_code
        if status_code.startswith("200"):
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


        else:
            body["status"] = "failure"
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

        return body

    def responseBody(self, status_code: str, msg: str = None, data: dict = {}):
        body = self.__generate_response_msg_from_code(status_code)
        body["reason"] = msg
        body["data"] = data
        return body
