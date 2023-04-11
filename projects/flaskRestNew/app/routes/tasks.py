from datetime import date, datetime, timedelta    
from app import celery
from app.database import db
import cx_Oracle
import json

@celery.task
def generate_logging(**kwargs):
    logging_args = kwargs
    
    print(logging_args,"----------------------------")
    cursor = db.get_cursor()
    connection = db.get_connection()
    out_val = cursor.var(str)
    # proc_list.append(out_val)
    logging_args.update({'v_result':out_val})

    
    cursor.callproc('JUS_J2CPOLLER.JUS_J2CTRANLOG',keywordParameters=logging_args)
    print(out_val.getvalue(),"=====================")
    connection.commit()

    return {"status": True} 
