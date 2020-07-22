import os, sys
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Config(object):
    SECRET_KEY = os.environ.get("SECRET_KEY")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    LOG_TO_STDOUT = os.environ.get('LOG_TO_STDOUT')
    # LANGUAGES = ['en', 'kr']


class ProductConfig(Config):
    DATABASE = {
        'USERNAME' : os.environ.get("DB_USERNAME"),
        'PASSWORD' : os.environ.get("DB_PASSWORD"),
        'HOST' : os.environ.get("DB_HOST"),
        'PORT' : os.environ.get("DB_PORT"),
        'SCHEMA' : os.environ.get("DB_SCHEMA")
    }
    SQLALCHEMY_DATABASE_URI = f"mysql+mysqlconnector://{DATABASE['USERNAME']}:{DATABASE['PASSWORD']}@{DATABASE['HOST']}/{DATABASE['SCHEMA']}"

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///test.db"

class LocalDevelopConfig(Config):
    SQLALCHEMY_DATABASE_URI = "sqlite:///dev.db"
    pass

class HerokuDevelopConfig(Config):
    # SQLALCHEMY_DATABASE_URI = f"sqlite:///dev.db"
    pass