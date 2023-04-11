from datetime import date
import cx_Oracle
import uuid
import json
from app.utils import random_digits

def default_logging_args():
    unique_uuid = str(uuid.uuid4())
    logging_args = {
        'v_id':'',
        'v_courtno':'',
        'v_action':'',
        'v_caseid':'',
        'v_chargeid':'',
        'v_operation':'GET',
        'v_dto_sent':'',
        'v_resp_dto':'{}',
        'v_resp_code':200,
        'v_resp_execid':unique_uuid,
        'v_resp_id':'',
        'v_create_ts':'',
        'v_tran_type':'CASE',
        'v_jus_guuid':'F79AD0E6B08A6C92E0535B33010A4230'
    }
    return logging_args
    