import datetime

from flask_script import Command

from app import db, create_app
from app.models.admin_models import Administrator
from app.models.common_models import CommonCode
from sqlalchemy import func
from config import *

import os, sys
from dotenv import load_dotenv
import secrets

from app.command.db_init import init_db

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

if __name__ == "__main__":
    app = create_app(HerokuDevelopConfig)
    # with app.app_context():
    #     init_db()

