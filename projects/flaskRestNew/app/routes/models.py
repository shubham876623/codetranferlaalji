from datetime import datetime
from app.database import localdb as db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, index=True, nullable=False)
    email = db.Column(db.String, unique=True, index=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now, index=True)

    __mapper_args__ = {
        "order_by": created_at
    }
    __tablename__ = 'user'

    def __repr__(self):
        return (
            '<{class_name}('
            'user_id={self.id}, '
            'username="{self.username}")>'.format(
                class_name=self.__class__.__name__,
                self=self
            )
        )
    
    def __init__(self,**kwargs):
        """Create a new user"""
        self.username = kwargs.get('username',None)
        self.email = kwargs.get('email',None)
        self.password = kwargs.get('password',None)
        