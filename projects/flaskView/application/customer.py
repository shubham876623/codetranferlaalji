import time
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from flask import jsonify
from flask import render_template, url_for, flash, redirect, request, send_file, send_from_directory
from flask_login import login_user, logout_user, login_required, current_user
from flask_sqlalchemy import sqlalchemy

from application import app, db
from application.models import User

import calendar
from sqlalchemy import extract

