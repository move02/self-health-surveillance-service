import os, sys
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Config(object):
    SECRET_KEY = os.environ.get("SECRET_KEY")
    DATABASE = {
        'USERNAME' : os.environ.get("DB_USERNAME"),
        'PASSWORD' : os.environ.get("DB_PASSWORD"),
        'HOST' : os.environ.get("DB_HOST"),
        'PORT' : os.environ.get("DB_PORT"),
        'SCHEMA' : os.environ.get("DB_SCHEMA")
    }
    SQLALCHEMY_DATABASE_URI = f"mysql+mysqlconnector://{DATABASE['USERNAME']}:{DATABASE['PASSWORD']}@{DATABASE['HOST']}/{DATABASE['SCHEMA']}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    LOG_TO_STDOUT = os.environ.get('LOG_TO_STDOUT')
    # LANGUAGES = ['en', 'kr']


class ProductConfig(Config):
    pass

class TestConfig(Config):
    pass

class DevelopConfig(Config):
    SQLALCHEMY_DATABASE_URI = f"sqlite:////temp/test.db"