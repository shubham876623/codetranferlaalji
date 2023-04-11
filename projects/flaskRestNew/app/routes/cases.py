from http import HTTPStatus
from flask import Blueprint, jsonify
from flask import request
from app.database import db, altdb
from flask_restful import Resource, reqparse, request
from app.routes.schemas import *
from flask_apispec.views import MethodResource
from flask_apispec import marshal_with, doc, use_kwargs
import requests
from app.routes.tasks import generate_logging
from app.routes.trans_logging import default_logging_args
import json
import cx_Oracle
from datetime import date




def convertBoolean(inputStr):
    if inputStr is None:
        return None
    if inputStr is not None and inputStr=='true':
        return True
    if inputStr is not None and inputStr=='false':
        return False

class CasesAPI(MethodResource,Resource):

    @classmethod
    def setApp(cls, app):
        cls.app = app
        return cls
    
    @doc(description='Cases Get API.', tags=['Cases'])
    # @marshal_with(CasesResSchema)
    def get(self,caseId):
        self.app.logger.info('Cases-Get: GET request')
        # Send logging to the asynchronous background task to the celery worker 
        logging_args = default_logging_args()
        logging_args.update({'v_tran_type':'CASE','v_operation':caseId})
        generate_logging.delay(**logging_args)
        cursor = altdb.get_cursor()
        out_val = cursor.var(cx_Oracle.DB_TYPE_CLOB)
        cursor.callproc('JUSAPI_CASES_PKG.jus_case_get',[str(caseId),"{}",out_val])
        responsed_clob = out_val.getvalue()
        print(responsed_clob,"----------------")
        # response = requests.get(f'https://ctrackupgrade.sftc.org/api/v1/cases/{caseId}', auth=('justisaccount', 'froM!notherplanet'),verify=False)

        # res_data = response.json()

        # logging_args = default_logging_args()
        # logging_args.update({'v_tran_type':'CASE','v_caseid':caseId,'v_resp_dto':json.dumps(res_data)})
        # generate_logging.delay(**logging_args)
        
        # return token
        return {}
    
    