from datetime import date
import cx_Oracle
from flask import Blueprint, jsonify
from flask import request
from app.database import localdb
from flask_restful import Resource, reqparse, request
from app.routes.schemas import UserReqSchema, UserSignUpReqSchema
from app.routes.models import User
from flask_apispec.views import MethodResource
from flask_apispec import marshal_with, doc, use_kwargs
from flask_jwt_extended import create_access_token, jwt_required, JWTManager
import json
import requests
import bcrypt



class UserSignUpAPI(MethodResource,Resource):

    @classmethod
    def setApp(cls, app):
        cls.app = app
        return cls
    
    @doc(description='SignUp API.', tags=['SignUp'])
    @use_kwargs(UserSignUpReqSchema)
    def post(self,**kwargs):
        # args = None
        self.app.logger.info('SignUp-Post: POST request')
        args = kwargs
        self.app.logger.info('SignUp-Post: args ' + str(args)) 
        username = args.get('username',None)
        email = args.get('email',None)
        password = args.get('password',None)

        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()) 
        user_req_data = {'username':username,'email':email,'password':hashed_password}

        user = User(**user_req_data)
        localdb.session.add(user)
        localdb.session.commit()
        return {'message': 'User has been created Successfully!'}



class UserSignInAPI(MethodResource,Resource):

    @classmethod
    def setApp(cls, app):
        cls.app = app
        return cls
    
    @doc(description='LogIn POST API.', tags=['User'])
    @use_kwargs(UserReqSchema)
    def post(self,**kwargs):
        # args = None
        self.app.logger.info('LogIn-Post: POST request')
        args = kwargs
        self.app.logger.info('LogIn-Post: args ' + str(args)) 
        username = args.get('username',None)
        password = args.get('password',None)
        user = User.query.filter_by(username=username).first()

        if user and bcrypt.checkpw(password.encode('utf-8'),user.password):
            user_id = getattr(user,'id')
            access_token = create_access_token(identity=user_id)
            return {'access_token':access_token}
        else:
            return {'message': 'Invalid credentials'}, 401