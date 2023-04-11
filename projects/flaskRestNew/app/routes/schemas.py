from marshmallow import Schema, fields
from app.database import db


class CourtReqSchema(Schema):
    CourtNo = fields.String(required=True)


class UserReqSchema(Schema):
    username = fields.String(required=True)
    password = fields.String(required=True)


class UserSignUpReqSchema(Schema):
    username = fields.String(required=True)
    email = fields.String(required=True)
    password = fields.String(required=True)


class CourtResSchema(Schema):
    CaseID = fields.Str()


class CasesResSchema(Schema):
    message = fields.Str(default='Success')
