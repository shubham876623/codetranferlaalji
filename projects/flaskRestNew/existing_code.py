from flask import Flask
from flask_cors import CORS, cross_origin

import uuid

import json

id = uuid.uuid4()
transactionId = str(id)

import logging
logFormatter = logging.Formatter("%(levelname)s:%(name)s:%(message)s")

logger=logging.getLogger()

# add console handler to the root logger
consoleHanlder = logging.StreamHandler()
consoleHanlder.setFormatter(logFormatter)
logger.addHandler(consoleHanlder)

# add file handler to the root logger
fileHandler = logging.FileHandler("CaseAPIlogs.log")
fileHandler.setFormatter(logFormatter)
logger.addHandler(fileHandler)
 
app = Flask(__name__)
CORS(app)

#from app import app
from flaskext.mysql import MySQL
 
mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] ='rahul123'
app.config['MYSQL_DATABASE_DB'] = 'casedetails'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

import pymysql
#from app import app
#from config import mysql
from flask import jsonify
from flask import flash, request

 
@app.route('/Cases', methods=['POST'])
def create_cases():
    app.logger.info("API Input Log- POST Method Request has been recived successfully by Flask API..." + "Below is the transactioID:   " + transactionId)
    
    try:
        app.logger.info("Backend Input Log- Request has been sent successfully to Database Table by Flask API..." + "Below is the transactioID:   " + transactionId )
        _json = request.json
        _caseid = _json['caseid']
        _client = _json['client']
        _status = _json['status']
        _defendent = _json['defendent']
        payload = json.dumps(_json)
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        if _caseid and _client and _status and _defendent and  request.method == 'POST':
            #conn = mysql.connect()
            #cursor = conn.cursor(pymysql.cursors.DictCursor)	
            Query = "INSERT INTO Cases(caseid,client,status,defendent) VALUES(%s, %s, %s ,%s)"
            Data = (_caseid,_client, _status,_defendent)            
            cursor.execute(Query,Data)
            app.logger.info("Backend Output Log- Resposne has been recived successfully from Database Table by Flask API..." + "Below is the transactioID:   " + transactionId + "\n" + payload)
            conn.commit()
            respone = jsonify('Case Details created successfully!')
            respone.status_code = 200
            app.logger.info("API Output Log- POST Method Response has been returned by Flask API successfully." + "Below is the transactioID:   " + transactionId ) 
            return respone
        else:
            return showMessage()
    except Exception as err:
        print(err)
    finally:
        cursor.close() 
        conn.close()  


@app.route('/Cases', methods=['PUT'])
def update_cases():
    try:
        _json = request.json
        _caseid = _json['caseid']
        _client = _json['client']
        _status = _json['status']
        _defendent = _json['defendent']
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        if _caseid and _client and _status and _defendent and  request.method == 'PUT':
            #conn = mysql.connect()
            #cursor = conn.cursor(pymysql.cursors.DictCursor)	
            Query = "UPDATE Cases SET caseid=%s,client=%s, status=%s,defendent=%s WHERE caseid=%s"
            Data = (_caseid,_client, _status,_defendent)            
            cursor.execute(Query,Data)
            conn.commit()
            respone = jsonify('Case Details updated successfully!')
            respone.status_code = 200
            return respone
        else:
            return showMessage()
    except Exception as err:
        print(err)
    finally:
        cursor.close() 
        conn.close()
        
             
    
@app.route('/Cases')
def Cases():
    app.logger.info("API Input Log- GET Method Request has been recived successfully by Flask API..." + "Below is the transactioID:  " + transactionId)
    try:
        app.logger.info("Backend Input Log- Request has been sent successfully to Database Table by Flask API..." + "Below is the transactioID:   " + transactionId)
    
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM Cases")
        stuRows = cursor.fetchall()
        app.logger.info("Backend Output Log- Resposne has been recived successfully from Database Table by Flask API..." + "Below is the transactioID:   " + transactionId)
        respone = jsonify(stuRows)
        respone.status_code = 200
        app.logger.info("API Output Log- GET Method Response has been returned by Flask API successfully." + "Below is the transactioID:   " + transactionId ) 
        return respone

    except Exception as err:
        print(err)
    finally:
        cursor.close() 
        conn.close()  

@app.route('/Cases/<int:caseid>', methods=['DELETE'])
def delete_Cases(caseid):
    app.logger.info("API Input Log- DELETE Method Request has been recived successfully by Flask API..." + "Below is the transactioID:   " + transactionId)
    try:
        app.logger.info("Backend Input Log- Request has been sent successfully to Database Table by Flask API..." + "Below is the transactioID:   " + transactionId)
    
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Cases WHERE caseid =%s", (caseid,))
        app.logger.info("Backend Output Log- Resposne has been recived successfully from Database Table by Flask API..." + "Below is the transactioID:   " + transactionId)
        conn.commit()
        respone = jsonify('Case details deleted successfully!')
        respone.status_code = 200
        app.logger.info("API Output Log- DELETE Method Response has been returned by Flask API successfully." + "Below is the transactioID:   " + transactionId ) 
        return respone

    except Exception as err:
        print(err)
    finally:
        cursor.close() 
        conn.close()
 

 

            
        
@app.errorhandler(404)
def showMessage(error=None):
    message = {
        'status': 404,
        'message': 'Record not found: ' + request.url,
    }
    respone = jsonify(message)
    respone.status_code = 404
    return respone
        
if __name__ == "__main__":
    app.run(debug=True)