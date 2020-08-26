import os, sys
from dotenv import load_dotenv
import secrets

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Config(object):
    SECRET_KEY = secrets.token_urlsafe(32)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    LOG_TO_STDOUT = os.environ.get('LOG_TO_STDOUT')
    SESSION_TYPE = "filesystem"
    # LANGUAGES = ['en', 'kr']



class ProductConfig(Config):
    DATABASE = {
        'USERNAME' : os.environ.get("DB_USERNAME"),
        'PASSWORD' : os.environ.get("DB_PASSWORD"),
        'HOST' : os.environ.get("DB_HOST"),
        'PORT' : os.environ.get("DB_PORT"),
        'SCHEMA' : os.environ.get("DB_SCHEMA")
    }
    SQLALCHEMY_DATABASE_URI = f"mysql+mysqldb://{DATABASE['USERNAME']}:{DATABASE['PASSWORD']}@{DATABASE['HOST']}:{DATABASE['PORT']}/{DATABASE['SCHEMA']}"

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///dev.db"

class LocalDevelopConfig(Config):
    SQLALCHEMY_DATABASE_URI = "sqlite:///dev.db"
    pass

class HerokuDevelopConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get("TINY_DATABASE_URI")
    pass