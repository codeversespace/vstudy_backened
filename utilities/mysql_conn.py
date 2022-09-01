# pip install mysqlclient
import MySQLdb
from configurations.configs import Creds
import json


class mysql_obj:

    # , host: str = 'localhost', user: str = None, passwd: str = None, db: str = None, conv: bool = True
    def __init__(self):
        self.host = Creds.MYSQL_HOST
        self.db = Creds.MYSQL_DB
        self.password = Creds.MYSQL_PASSWORD
        self.user = Creds.MYSQL_USER
        # conv = conversions.copy()
        # if conv:
        #     conv[246] = float  # convert decimals to floats
        #     conv[7] = str  # convert dates to strings
        #     conv[10] = str
        # self.conn.cursor()
        self.conn = MySQLdb.connect(host=self.host,  # your host, usually localhost
                                    user=self.user,  # your username
                                    passwd=self.password,  # your password
                                    db=self.db,  # conv=conv
                                    )

    def close(self):
        return self.conn.close()

    def commit(self):
        return self.conn.commit()

    def mysql_cursor(self):
        return self.conn.cursor()

    # if data not exists it will return 0
    def mysql_execute(self, query, fetch_result: bool = True):
        cursor = self.mysql_cursor()
        if fetch_result:
            cursor.execute(query)
            return self.mysql_fetchall(cursor)
        return cursor.execute(query)

    def mysql_fetchall(self, cursor):
        row_headers = [x[0] for x in cursor.description]  # this will extract row headers
        rv = cursor.fetchall()
        json_data = []
        for result in rv:
            json_data.append(dict(zip(row_headers, result)))
        return json_data

    def if_exist(self, table: str, column: str, value: str):
        q = f"select 1 from {table} WHERE {column} = '{value}' limit 1"
        return self.mysql_execute(q, False)
