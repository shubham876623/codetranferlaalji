from application import db, ma, login_manager
from marshmallow import Schema, fields


class UserSchema(ma.Schema):
    class Meta:
        fields = ("id", "lastname", "surname", "phonenumber", "email", "image_file", "is_admin", "teller", "password",
                  "unique_id", "is_specialist", "date_added", "branch_unique")

