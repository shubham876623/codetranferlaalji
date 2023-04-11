from celery import Celery
from flask import Flask
from flask_restful import Resource, Api
from app.utils import get_config
import logging
from flask_cors import CORS, cross_origin
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from flask_apispec.extension import FlaskApiSpec
from flask_jwt_extended import create_access_token, jwt_required, JWTManager


fileHandler = logging.FileHandler("api_logs.log")
logFormatter = logging.Formatter("%(levelname)s:%(name)s:%(message)s")
fileHandler.setFormatter(logFormatter)
fileHandler.setLevel(logging.INFO)


Config = get_config()
celery = Celery(__name__, broker=Config.CELERY_BROKER_URL)


def make_celery(app):
    celery = Celery(
        app.import_name,
        backend=app.config['CELERY_RESULT_BACKEND'],
        broker=app.config['CELERY_BROKER_URL']
    )
    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery

SECRET_KEY = 'anotherplanet-secret'

def create_app(config_name=None, **kwargs):
    """
    Entry point to the Flask RESTful Server application.
    """
    from app.routes.court import CourtAPI
    from app.routes.cases import CasesAPI
    from app.routes.users import UserSignInAPI, UserSignUpAPI 
    from app.database import init_db
    app = Flask(__name__, **kwargs)
    app.config['JWT_SECRET_KEY'] = SECRET_KEY
    jwt = JWTManager(app)

    try:
        app.config.from_object(get_config(config_name))
    except ImportError:
        raise Exception('Invalid Config')
    
    api = Api(app)
    
    if app.config['DEBUG'] == True or app.config['TESTING'] == True:
        CORS(app)
    # Applying configuration for swagger API doc
    app.config.update({ 
        'APISPEC_SPEC': APISpec(
            title='JUSTIS System API',
            version='v1',
            plugins=[MarshmallowPlugin()],
            openapi_version='2.0.0'
        ),
        'APISPEC_SWAGGER_URL': '/swagger/',
        'APISPEC_SWAGGER_UI_URL': '/swagger-ui/'
    })
    docs = FlaskApiSpec(app)
    
    courtAPI = CourtAPI.setApp(app)
    api.add_resource(courtAPI, '/api/court')

    casesAPI = CasesAPI.setApp(app)
    api.add_resource(casesAPI, '/api/cases/<int:caseId>')

    userSignUpAPI = UserSignUpAPI.setApp(app)
    api.add_resource(userSignUpAPI, '/api/user/signup')

    userSignInAPI = UserSignInAPI.setApp(app)
    api.add_resource(userSignInAPI, '/api/user/login')

    docs.register(courtAPI)
    docs.register(casesAPI)
    docs.register(userSignInAPI)
    docs.register(userSignUpAPI)

    init_db(app)
    app.config.update(
        CELERY_BROKER_URL='redis://localhost:6379',
        CELERY_RESULT_BACKEND='redis://localhost:6379',
        CELERY_ACCEPT_CONTENT=['application/json'],
        CELERY_TASK_SERIALIZER='json',
        CELERY_TIMEZONE='Asia/Kolkata'
    )
    celery = make_celery(app)
    app.logger.setLevel(logging.INFO)
    app.logger.addHandler(fileHandler)
    return app