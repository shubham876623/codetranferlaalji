from datetime import date
import cx_Oracle
from app.database import db
from flask_restful import Resource
from app.routes.schemas import CourtReqSchema, CourtResSchema
from flask_apispec.views import MethodResource
from flask_apispec import marshal_with, doc, use_kwargs
import json
import requests
from app.routes.tokenauth import token_required
from app.routes.tasks import generate_logging
from app.routes.trans_logging import default_logging_args
import uuid




def convertBoolean(inputStr):
    if inputStr is None:
        return None
    if inputStr is not None and inputStr=='true':
        return True
    if inputStr is not None and inputStr=='false':
        return False

class CourtAPI(MethodResource,Resource):

    @classmethod
    def setApp(cls, app):
        cls.app = app
        return cls
    
    @doc(description='Court POST API.', tags=['Court'])
    @use_kwargs(CourtReqSchema)
    # @token_required
    def post(self,**kwargs):
        # args = None
        self.app.logger.info('Court-Post: POST request')
        args = kwargs
        self.app.logger.info('Court-Post: args ' + str(args)) 
        CourtNo = args.get('CourtNo')
        CourtNo = str(CourtNo).zfill(8)
        # Send logging to the asynchronous background task to the celery worker 
        logging_args = default_logging_args()
        logging_args.update({'v_tran_type':'CASE','v_operation':'POST','v_courtno':CourtNo})
        generate_logging.delay(**logging_args)
        cursor = db.get_cursor()
        out_val = cursor.var(cx_Oracle.DB_TYPE_CLOB)
        cursor.callproc('JUSCOURT_CASES_PKG.CASE_CASEDATA_COURTNO_JSON',[CourtNo,out_val])
        responsed_clob = out_val.getvalue()
        formatted_data = {
            "caseClassificationID": "5000000",
            "caseNumber": "CRI-23004465",
            "security4": "false",
            "security5": "false",
            "alternateCaseNumbers": [
                {
                    "alternateCaseNumber": "23004465",
                    "alternateCaseNumberType": "5000043"
                }
            ],
            "submittedDate": "2023-03-26T01:17:00", 
            "security1": "false",
            "security2": "false",
            "security3": "false"
        }
        today = date.today()
        submittedDate = today.strftime("%Y-%m-%dT%H:%M:%S")
        responsed_json = json.loads(responsed_clob.read())
        logging_args = default_logging_args()
        logging_args.update({'v_tran_type':'CASE','v_operation':'POST','v_resp_dto':json.dumps(responsed_json),'v_courtno':CourtNo})
        generate_logging.delay(**logging_args)
        caseData = responsed_json.get('caseData',{})
        formatted_data.update({'caseClassificationID':caseData.get('caseClassificationID',None),'caseNumber':caseData.get('caseNumber',None),'security1':convertBoolean(caseData.get('security1',None)),'security2':convertBoolean(caseData.get('security2',None)),'security3':convertBoolean(caseData.get('security3',None)),'security4':convertBoolean(caseData.get('security4',None)),'security5':convertBoolean(caseData.get('security5',None)),'alternateCaseNumbers':caseData.get('alternateCaseNumbers',[]),'submittedDate':submittedDate})
        logging_args = default_logging_args()
        logging_args.update({'v_tran_type':'CASE','v_operation':'POST','v_courtno':CourtNo})
        generate_logging.delay(**logging_args)

        resp = requests.post('https://ctrackupgrade.sftc.org/api/v1/cases', data=json.dumps(formatted_data), auth=('justisaccount', 'froM!notherplanet'),verify=False,headers={'Content-Type': 'application/json'})

        try:
            resp_caseid = resp.headers.__dict__['_store'].get('id')[1]
            logging_args = default_logging_args()
            logging_args.update({'v_tran_type':'CASE','v_operation':'POST','v_caseid':resp_caseid,'v_courtno':CourtNo})
            generate_logging.delay(**logging_args)
            return {'CaseId':(resp_caseid)}
        except Exception as resp_err:
            error_message = resp.json().get('validationErrors')
            return {'exception': error_message}, 400

