# app 시작 시
import logging
from logging.handlers import RotatingFileHandler
import os
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from flask_cors import CORS, cross_origin
from flask_wtf.csrf import CSRFProtect
from flask_user import UserManager

from config import *
from dotenv import load_dotenv

import json
from .error_handlers import *

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

db = SQLAlchemy()
migrate = Migrate()
csrf = CSRFProtect()

def create_app(config_class=Config):
    app = Flask(
        __name__,
        static_url_path=''
    )
    app.config.from_object(config_class)
    app.register_error_handler(404, page_not_found)
    app.register_error_handler(500, internal_error)

    db.init_app(app)
    csrf.init_app(app)
    migrate.init_app(app, db)
    CORS(app, resources={r'*': {'origins': 'http://localhost:5000'}})

    if not app.debug and not app.testing:
        if app.config['LOG_TO_STDOUT']:
            stream_handler = logging.StreamHandler()
            stream_handler.setLevel(logging.INFO)
            app.logger.addHandler(stream_handler)
        else:   
            if not os.path.exists('logs'):
                os.mkdir('logs')
            file_handler = RotatingFileHandler('logs/app.log', maxBytes=10240, backupCount=10)
            file_handler.setFormatter(logging.Formatter(
                '%(asctime)s %(levelname)s: %(message)s '
                '[in %(pathname)s:%(lineno)d]'))
            file_handler.setLevel(logging.INFO)
            app.logger.addHandler(file_handler)
    
        app.logger.setLevel(logging.INFO)
        app.logger.info("Myapp Startup")

    return app


app = None
current_env = os.environ.get("CURRENT_ENV")

if current_env == "LocalDevelop":
    app = create_app(LocalDevelopConfig)
elif current_env == "HerokuDevelop":
    app = create_app(HerokuDevelopConfig)
elif current_env == "Test":
    app = create_app(TestConfig)
elif current_env == "Product":
    app = create_app(ProductConfig)

## .env 를 볼 수 없는 상황
else:
    # app = create_app(HerokuDevelopConfig)
    raise EnvironmentError

from app.models.mymodel import *
from app import views

from app.command import db_init
with app.app_context():
    db.init_app(app)
    db_init.init_db()

user_manager = UserManager(app, db, Administrators)