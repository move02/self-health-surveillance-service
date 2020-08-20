# app 시작 시
import logging
from logging.handlers import RotatingFileHandler
import os
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from flask_cors import CORS, cross_origin
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager
from flask_session import Session

from config import *
from dotenv import load_dotenv
from flask_bcrypt import Bcrypt #암호화

import json
from .error_handlers import *

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

db = SQLAlchemy()
migrate = Migrate()
csrf = CSRFProtect()
login_manager = LoginManager()
bcrypt = Bcrypt()
sess = Session()

from .admin_views.general import general_view
from .admin_views.login import login_view
from .admin_views.main import main_view
from .admin_views.system import system_view

def create_app(config_class=Config):
    app = Flask(
        __name__,
        static_url_path=''
    )
    app.config.from_object(config_class)
    app.secret_key = Config.SECRET_KEY
    app.register_error_handler(404, page_not_found)
    app.register_error_handler(500, internal_error)

    ## Blueprint
    app.register_blueprint(general_view, url_prefix="/admin")
    app.register_blueprint(login_view, url_prefix="/admin/login")
    app.register_blueprint(main_view, url_prefix="/admin")
    app.register_blueprint(system_view, url_prefix="/system")

    ## login manager setting
    login_manager.login_view = "login.login"
    login_manager.register_view = "login.register"
    login_manager.login_message = None

    db.init_app(app)
    csrf.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    sess.init_app(app)

    #암호화
    bcrypt.init_app(app)

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

from app.models.admin_models import *
from app import admin_views
from app import userViews
from app import utils
