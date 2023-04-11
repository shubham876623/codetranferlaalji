import cx_Oracle
from sqlalchemy import create_engine
from sqlalchemy.engine import url
from sqlalchemy.orm import sessionmaker
from flask_sqlalchemy import SQLAlchemy


localdb = SQLAlchemy()


def init_db(app):
    with app.app_context():
        localdb.init_app(app)
        localdb.create_all()

# jdbc:oracle:thin:@10.1.51.92

DB_HOST = '10.1.62.97'
DB_PORT = '1521'
DB_SERVICE_NAME = 'jusCourtspdb.sfjustis.sfgov.org'
DB_USERNAME = 'courtadmin'
DB_PASSWORD = 'courtadmin1234$'


# ALT_DB_HOST = '10.1.62.83'
ALT_DB_HOST = '10.1.62.64'

ALT_DB_PORT = '1521'
#ALT_DB_SERVICE_NAME='jusstg'
# ALT_DB_SERVICE_NAME = 'pdb_jusstg.sfjustis.sfgov.org'
ALT_DB_SERVICE_NAME = 'orclpdb.sfjustis.sfgov.org'
ALT_DB_USERNAME = 'justisdl'
ALT_DB_PASSWORD = 'Jusdltst'




class OracleDB():

    def __init__(self,**kwargs):
        self.cursor = None
        self.con = None
        self.DB_HOST = kwargs.get('DB_HOST')
        self.DB_PORT = kwargs.get('DB_PORT')
        self.DB_SERVICE_NAME = kwargs.get('DB_SERVICE_NAME')
        self.DB_USERNAME = kwargs.get('DB_USERNAME')
        self.DB_PASSWORD = kwargs.get('DB_PASSWORD')
        


    def get_cursor(self):
        try:
            dsnStr = cx_Oracle.makedsn(self.DB_HOST, self.DB_PORT,service_name=self.DB_SERVICE_NAME)
            connection = cx_Oracle.connect(user=self.DB_USERNAME, password=self.DB_PASSWORD, dsn=dsnStr,encoding="UTF-8")
            self.con = connection
            cursor = self.con.cursor()
            self.cursor = cursor
            return  cursor
        except Exception as error:
            print("There is a problem with Oracle =====", error)
            return None
    
    def get_connection(self):
        return self.con
    
    def close_conn(self):
        if self.cursor is not None:
            self.cursor.close()
        if self.con is not None:
            self.con.close()

db = OracleDB(DB_HOST=DB_HOST,DB_USERNAME=DB_USERNAME,DB_PASSWORD=DB_PASSWORD,DB_SERVICE_NAME=DB_SERVICE_NAME,DB_PORT=DB_PORT)

altdb = OracleDB(DB_HOST=ALT_DB_HOST,DB_USERNAME=ALT_DB_USERNAME,DB_PASSWORD=ALT_DB_PASSWORD,DB_SERVICE_NAME=ALT_DB_SERVICE_NAME,DB_PORT=ALT_DB_PORT)