from app.utilities import mysql_conn


class GetCode:
    def subject(self, sub_str: str = None):
        m_conn = mysql_conn.mysql_obj()
        query = f"SELECT sub_id FROM subject WHERE sub_title = '{sub_str}'"
        data = m_conn.mysql_execute(query, fetch_result=True)
        m_conn.close()
        if len(data) < 1:
            return 3333
        sub_id = data[0]['sub_id']
        return sub_id

    def subjectById(self, sub_str: str = None):
        m_conn = mysql_conn.mysql_obj()
        query = f"SELECT sub_title FROM subject WHERE sub_id = '{sub_str}'"
        data = m_conn.mysql_execute(query, fetch_result=True)
        m_conn.close()
        if len(data) < 1:
            return 'Unknown Subject'
        sub_title = data[0]['sub_title']
        return sub_title

    # def schoolDetail(self, school_id: int = None):
    #     m_conn = mysql_conn.mysql_obj()
    #     query = f"SELECT sub_title FROM subject WHERE sub_id = '{sub_str}'"
    #     data = m_conn.mysql_execute(query, fetch_result=True)
    #     m_conn.close()
    #     if len(data) < 1:
    #         return 'Unknown Subject'
    #     sub_title = data[0]['sub_title']
    #     return sub_title



getCode = GetCode()
