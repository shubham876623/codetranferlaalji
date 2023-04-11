import os
import random
import string
from random import randint
from werkzeug.utils import import_string

CONFIG_NAME_MAPPER = {
    'development': 'config.DevelopmentConfig',
    'testing': 'config.TestingConfig',
}


def get_config(config_name=None):
    flask_config_name = os.getenv('FLASK_CONFIG', 'development')
    if config_name is not None:
        flask_config_name = config_name
    return import_string(CONFIG_NAME_MAPPER[flask_config_name])



def random_digits():
    range_start = 10**(8-1)
    range_end = (10**8)-1
    return randint(range_start, range_end)