import cx_Oracle
from sqlalchemy import create_engine
from sqlalchemy.engine import url
from sqlalchemy.orm import sessionmaker
from flask_sqlalchemy import SQLAlchemy


localdb = SQLAlchemy()


# jdbc:oracle:thin:@10.1.51.92

DB_HOST = '10.1.62.97'
PORT = '1521'
SERVICE_NAME = 'jusCourtspdb.sfjustis.sfgov.org'
DB_USERNAME = 'courtadmin'
DB_PASSWORD = 'courtadmin1234$'


class OracleDB():

    def __init__(self):
        self.cursor = None
        self.con = None

    def get_cursor(self):
        try:
            dsnStr = cx_Oracle.makedsn(DB_HOST, PORT,service_name=SERVICE_NAME)
            connection = cx_Oracle.connect(user=DB_USERNAME, password=DB_PASSWORD, dsn=dsnStr,encoding="UTF-8")
            self.con = connection
            cursor = self.con.cursor()
            self.cursor = cursor
            return  cursor
        except Exception as error:
            print("There is a problem with Oracle", error)
            return None
    
    def get_connection(self):
        return self.con
    
    def close_conn(self):
        if self.cursor is not None:
            self.cursor.close()
        if self.con is not None:
            self.con.close()

db = OracleDB()